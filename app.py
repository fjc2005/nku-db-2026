from flask import Flask, render_template, request

from db import execute_write, fetch_all, fetch_one, get_connection


STAT_QUERIES = [
    {
        "label": "学生数",
        "sql": "SELECT COUNT(*) AS count_value FROM students",
    },
    {
        "label": "饮品数",
        "sql": "SELECT COUNT(*) AS count_value FROM drinks",
    },
    {
        "label": "进行中拼单",
        "sql": "SELECT COUNT(*) AS count_value FROM group_orders WHERE status = %s",
        "params": ("OPEN",),
    },
]


def load_home_stats():
    stats = []
    for item in STAT_QUERIES:
        row = fetch_one(item["sql"], item.get("params"))
        stats.append(
            {
                "label": item["label"],
                "value": row["count_value"],
                "status": "来自 MySQL",
            }
        )
    return stats


def fallback_stats():
    return [
        {"label": item["label"], "value": "--", "status": "数据库暂不可用"}
        for item in STAT_QUERIES
    ]


def empty_order_form_options():
    return {
        "students": [],
        "group_orders": [],
        "drinks": [],
        "coupons": [],
    }


def load_order_form_options():
    return {
        "students": fetch_all(
            """
            SELECT student_id, student_no, name, status
            FROM students
            ORDER BY CASE WHEN status = 'ACTIVE' THEN 0 ELSE 1 END, student_id
            """
        ),
        "group_orders": fetch_all(
            """
            SELECT
                go.group_order_id,
                go.title,
                go.status,
                sh.shop_name
            FROM group_orders go
            JOIN shops sh ON go.shop_id = sh.shop_id
            ORDER BY CASE WHEN go.status = 'OPEN' THEN 0 ELSE 1 END, go.group_order_id
            """
        ),
        "drinks": fetch_all(
            """
            SELECT
                d.drink_id,
                d.drink_name,
                d.price,
                d.stock,
                d.status,
                sh.shop_name
            FROM drinks d
            JOIN shops sh ON d.shop_id = sh.shop_id
            ORDER BY CASE WHEN d.status = 'ON_SALE' THEN 0 ELSE 1 END, d.drink_id
            """
        ),
        "coupons": fetch_all(
            """
            SELECT
                c.coupon_id,
                c.coupon_name,
                c.amount,
                c.status,
                s.student_no,
                s.name AS student_name
            FROM coupons c
            JOIN students s ON c.student_id = s.student_id
            ORDER BY CASE WHEN c.status = 'UNUSED' THEN 0 ELSE 1 END, c.coupon_id
            """
        ),
    }


def parse_int(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError("请输入有效数字") from exc


def parse_required_positive_int(value, field_label):
    parsed_value = parse_int(value)
    if parsed_value is None:
        raise ValueError(f"{field_label}不能为空")
    if parsed_value <= 0:
        raise ValueError(f"{field_label}必须为正整数")
    return parsed_value


def parse_optional_positive_int(value, field_label):
    parsed_value = parse_int(value)
    if parsed_value is None:
        return None
    if parsed_value <= 0:
        raise ValueError(f"{field_label}必须为正整数")
    return parsed_value


def extract_error_reason(exc):
    message = getattr(exc, "msg", None) or str(exc)
    message = (message or "数据库操作失败，请检查输入和数据库状态。").strip()
    if not message:
        return "数据库操作失败，请检查输入和数据库状态。"

    first_line = message.splitlines()[0].strip()
    if "): " in first_line:
        first_line = first_line.split("): ", 1)[1].strip()
    if "Traceback" in first_line:
        return "数据库操作失败，请检查输入和数据库状态。"
    return first_line


def operation_error(prefix, exc):
    return f"{prefix}：{extract_error_reason(exc)}"


def finish_group_order(group_order_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.callproc("sp_finish_group_order", (group_order_id,))
        for result in cursor.stored_results():
            result.fetchall()
        connection.commit()
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def cancel_group_order_transaction(group_order_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        connection.start_transaction()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT group_order_id, status
            FROM group_orders
            WHERE group_order_id = %s
            FOR UPDATE
            """,
            (group_order_id,),
        )
        group_order = cursor.fetchone()
        if group_order is None:
            raise ValueError("拼单不存在")

        if group_order["status"] == "FINISHED":
            raise ValueError("已完成拼单不能取消")
        if group_order["status"] == "CANCELED":
            raise ValueError("已取消拼单不能取消")
        if group_order["status"] != "OPEN":
            raise ValueError("拼单不是进行中状态，不能取消")

        cursor.execute(
            """
            SELECT COUNT(*) AS item_count
            FROM order_items
            WHERE group_order_id = %s
            """,
            (group_order_id,),
        )
        item_count = cursor.fetchone()["item_count"]
        if item_count == 0:
            raise ValueError("拼单没有订单明细，不能取消")

        cursor.execute(
            """
            UPDATE drinks d
            JOIN (
                SELECT drink_id, SUM(quantity) AS restore_quantity
                FROM order_items
                WHERE group_order_id = %s
                GROUP BY drink_id
            ) item_summary ON d.drink_id = item_summary.drink_id
            SET d.stock = d.stock + item_summary.restore_quantity
            """,
            (group_order_id,),
        )
        restored_drink_rows = cursor.rowcount

        cursor.execute(
            """
            UPDATE coupons c
            JOIN order_items oi ON c.coupon_id = oi.coupon_id
            SET c.status = 'UNUSED'
            WHERE oi.group_order_id = %s
              AND oi.coupon_id IS NOT NULL
            """,
            (group_order_id,),
        )
        restored_coupon_rows = cursor.rowcount

        cursor.execute(
            """
            DELETE oi
            FROM order_items oi
            JOIN group_orders go ON oi.group_order_id = go.group_order_id
            WHERE go.group_order_id = %s
            """,
            (group_order_id,),
        )
        deleted_item_rows = cursor.rowcount

        cursor.execute(
            """
            DELETE FROM group_orders
            WHERE group_order_id = %s
            """,
            (group_order_id,),
        )
        deleted_group_rows = cursor.rowcount
        if deleted_group_rows != 1:
            raise ValueError("拼单主记录删除失败")

        cursor.execute(
            """
            INSERT INTO operation_logs (op_type, detail)
            VALUES (%s, %s)
            """,
            (
                "CANCEL_GROUP_ORDER",
                (
                    f"group_order_id={group_order_id}, "
                    f"deleted_items={deleted_item_rows}, "
                    f"restored_drinks={restored_drink_rows}, "
                    f"restored_coupons={restored_coupon_rows}"
                ),
            ),
        )

        connection.commit()
        return {
            "deleted_items": deleted_item_rows,
            "restored_drinks": restored_drink_rows,
            "restored_coupons": restored_coupon_rows,
        }
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def query_group_order_details(filters):
    where_clauses = []
    params = []

    group_order_id = parse_int(filters["group_order_id"])
    if group_order_id is not None:
        where_clauses.append("group_order_id = %s")
        params.append(group_order_id)

    student_name = filters["student_name"].strip()
    if student_name:
        where_clauses.append("student_name LIKE %s")
        params.append(f"%{student_name}%")

    group_status = filters["group_status"].strip()
    if group_status:
        if group_status not in {"OPEN", "FINISHED", "CANCELED"}:
            raise ValueError("拼单状态不正确")
        where_clauses.append("group_status = %s")
        params.append(group_status)

    sql = """
        SELECT
            group_order_id,
            group_title,
            group_status,
            group_total_amount,
            shop_name,
            order_item_id,
            student_no,
            student_name,
            drink_name,
            drink_price,
            quantity,
            item_amount,
            discount_amount,
            pay_amount,
            item_status
        FROM v_group_order_detail
    """
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY group_order_id, order_item_id"
    return fetch_all(sql, tuple(params))


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        database_error = None
        try:
            stats = load_home_stats()
        except Exception:
            stats = fallback_stats()
            database_error = "数据库暂时不可用，请确认 MySQL 已启动并已导入 schema.sql。"

        actions = [
            {
                "title": "加入拼单",
                "description": "演示触发器控制下的订单明细插入。",
                "href": "/order/add",
            },
            {
                "title": "完成拼单",
                "description": "演示存储过程控制下的拼单更新。",
                "href": "/group/finish",
            },
            {
                "title": "取消拼单",
                "description": "演示显式事务控制下的拼单删除。",
                "href": "/group/cancel",
            },
            {
                "title": "拼单详情查询",
                "description": "演示基于视图的多表查询。",
                "href": "/group/query",
            },
        ]
        return render_template(
            "index.html",
            actions=actions,
            database_error=database_error,
            stats=stats,
        )

    @app.route("/data/students")
    def data_students():
        rows = []
        message = None
        message_type = None
        try:
            rows = fetch_all(
                """
                SELECT student_id, student_no, name, phone, status
                FROM students
                ORDER BY student_id
                """
            )
        except Exception:
            message = "学生数据暂时不可用，请确认数据库连接和表结构。"
            message_type = "error"

        return render_template(
            "data_students.html",
            rows=rows,
            message=message,
            message_type=message_type,
        )

    @app.route("/data/shops")
    def data_shops():
        rows = []
        message = None
        message_type = None
        try:
            rows = fetch_all(
                """
                SELECT shop_id, shop_name, campus_location, status
                FROM shops
                ORDER BY shop_id
                """
            )
        except Exception:
            message = "店铺数据暂时不可用，请确认数据库连接和表结构。"
            message_type = "error"

        return render_template(
            "data_shops.html",
            rows=rows,
            message=message,
            message_type=message_type,
        )

    @app.route("/data/drinks")
    def data_drinks():
        rows = []
        message = None
        message_type = None
        try:
            rows = fetch_all(
                """
                SELECT
                    d.drink_id,
                    sh.shop_name,
                    d.drink_name,
                    d.price,
                    d.stock,
                    d.status
                FROM drinks d
                JOIN shops sh ON d.shop_id = sh.shop_id
                ORDER BY d.drink_id
                """
            )
        except Exception:
            message = "饮品数据暂时不可用，请确认数据库连接和表结构。"
            message_type = "error"

        return render_template(
            "data_drinks.html",
            rows=rows,
            message=message,
            message_type=message_type,
        )

    @app.route("/data/coupons")
    def data_coupons():
        rows = []
        message = None
        message_type = None
        try:
            rows = fetch_all(
                """
                SELECT
                    c.coupon_id,
                    s.name AS student_name,
                    c.coupon_name,
                    c.amount,
                    c.min_order_amount,
                    c.valid_until,
                    c.status
                FROM coupons c
                JOIN students s ON c.student_id = s.student_id
                ORDER BY c.coupon_id
                """
            )
        except Exception:
            message = "优惠券数据暂时不可用，请确认数据库连接和表结构。"
            message_type = "error"

        return render_template(
            "data_coupons.html",
            rows=rows,
            message=message,
            message_type=message_type,
        )

    @app.route("/logs")
    def operation_logs():
        rows = []
        message = None
        message_type = None
        try:
            rows = fetch_all(
                """
                SELECT log_id, op_type, detail, created_at
                FROM operation_logs
                ORDER BY created_at DESC, log_id DESC
                """
            )
        except Exception:
            message = "操作日志暂时不可用，请确认数据库连接和表结构。"
            message_type = "error"

        return render_template(
            "operation_logs.html",
            rows=rows,
            message=message,
            message_type=message_type,
        )

    @app.route("/order/add", methods=["GET", "POST"])
    def add_order():
        form_data = {
            "group_order_id": "1",
            "student_id": "1",
            "drink_id": "1",
            "quantity": "1",
            "coupon_id": "1",
        }
        message = None
        message_type = None
        options = empty_order_form_options()
        options_error = None

        try:
            options = load_order_form_options()
        except Exception:
            options_error = "下拉选项暂时不可用，请确认数据库连接和基础数据。"

        if request.method == "POST":
            form_data = {
                "group_order_id": request.form.get("group_order_id", "").strip(),
                "student_id": request.form.get("student_id", "").strip(),
                "drink_id": request.form.get("drink_id", "").strip(),
                "quantity": request.form.get("quantity", "").strip(),
                "coupon_id": request.form.get("coupon_id", "").strip(),
            }
            try:
                group_order_id = parse_required_positive_int(
                    form_data["group_order_id"], "拼单编号"
                )
                student_id = parse_required_positive_int(
                    form_data["student_id"], "学生编号"
                )
                drink_id = parse_required_positive_int(
                    form_data["drink_id"], "饮品编号"
                )
                coupon_id = parse_optional_positive_int(
                    form_data["coupon_id"], "优惠券编号"
                )
                quantity = parse_required_positive_int(
                    form_data["quantity"], "购买数量"
                )

                order_item_id = execute_write(
                    """
                    INSERT INTO order_items (
                        group_order_id,
                        student_id,
                        drink_id,
                        coupon_id,
                        quantity
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (group_order_id, student_id, drink_id, coupon_id, quantity),
                )
                message = f"加入拼单成功，订单明细编号：{order_item_id}"
                message_type = "success"
            except ValueError as exc:
                message = str(exc) or "请输入有效数字"
                message_type = "error"
            except Exception as exc:
                message = operation_error("加入拼单失败", exc)
                message_type = "error"

        return render_template(
            "add_order.html",
            form_data=form_data,
            message=message,
            message_type=message_type,
            options=options,
            options_error=options_error,
        )

    @app.route("/group/finish", methods=["GET", "POST"])
    def finish_group():
        form_data = {"group_order_id": "2"}
        message = None
        message_type = None

        if request.method == "POST":
            form_data = {
                "group_order_id": request.form.get("group_order_id", "").strip()
            }
            try:
                group_order_id = parse_required_positive_int(
                    form_data["group_order_id"], "拼单编号"
                )

                finish_group_order(group_order_id)
                message = "拼单完成成功"
                message_type = "success"
            except ValueError as exc:
                message = str(exc)
                message_type = "error"
            except Exception as exc:
                message = operation_error("拼单完成失败", exc)
                message_type = "error"

        return render_template(
            "finish_group.html",
            form_data=form_data,
            message=message,
            message_type=message_type,
        )

    @app.route("/group/cancel", methods=["GET", "POST"])
    def cancel_group():
        form_data = {"group_order_id": "5"}
        message = None
        message_type = None

        if request.method == "POST":
            form_data = {
                "group_order_id": request.form.get("group_order_id", "").strip()
            }
            try:
                group_order_id = parse_required_positive_int(
                    form_data["group_order_id"], "拼单编号"
                )

                summary = cancel_group_order_transaction(group_order_id)
                message = (
                    "取消拼单成功，"
                    f"删除明细 {summary['deleted_items']} 条，"
                    f"恢复饮品 {summary['restored_drinks']} 类，"
                    f"恢复优惠券 {summary['restored_coupons']} 张"
                )
                message_type = "success"
            except ValueError as exc:
                message = str(exc)
                message_type = "error"
            except Exception as exc:
                message = operation_error("取消拼单失败", exc)
                message_type = "error"

        return render_template(
            "cancel_group.html",
            form_data=form_data,
            message=message,
            message_type=message_type,
        )

    @app.route("/group/query")
    def query_group():
        filters = {
            "group_order_id": request.args.get("group_order_id", "").strip(),
            "student_name": request.args.get("student_name", "").strip(),
            "group_status": request.args.get("group_status", "").strip(),
        }
        rows = []
        message = None
        message_type = None

        try:
            rows = query_group_order_details(filters)
            if not rows:
                message = "没有查询到匹配的拼单详情"
                message_type = "empty"
        except ValueError as exc:
            message = str(exc)
            message_type = "error"
        except Exception as exc:
            message = operation_error("查询失败", exc)
            message_type = "error"

        return render_template(
            "query_group.html",
            filters=filters,
            message=message,
            message_type=message_type,
            rows=rows,
            status_options=("OPEN", "FINISHED", "CANCELED"),
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
