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


def parse_int(value):
    value = value.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError("请输入有效数字") from exc


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

        if request.method == "POST":
            form_data = {
                "group_order_id": request.form.get("group_order_id", "").strip(),
                "student_id": request.form.get("student_id", "").strip(),
                "drink_id": request.form.get("drink_id", "").strip(),
                "quantity": request.form.get("quantity", "").strip(),
                "coupon_id": request.form.get("coupon_id", "").strip(),
            }
            try:
                params = (
                    parse_int(form_data["group_order_id"]),
                    parse_int(form_data["student_id"]),
                    parse_int(form_data["drink_id"]),
                    parse_int(form_data["coupon_id"]),
                    parse_int(form_data["quantity"]),
                )
                if any(value is None for value in params[:3]) or params[4] is None:
                    raise ValueError("拼单编号、学生编号、饮品编号和购买数量不能为空")

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
                    params,
                )
                message = f"加入拼单成功，订单明细编号：{order_item_id}"
                message_type = "success"
            except ValueError as exc:
                message = str(exc) or "请输入有效数字"
                message_type = "error"
            except Exception as exc:
                message = f"加入拼单失败：{exc}"
                message_type = "error"

        return render_template(
            "add_order.html",
            form_data=form_data,
            message=message,
            message_type=message_type,
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
                group_order_id = parse_int(form_data["group_order_id"])
                if group_order_id is None:
                    raise ValueError("拼单编号不能为空")

                finish_group_order(group_order_id)
                message = "拼单完成成功"
                message_type = "success"
            except ValueError as exc:
                message = str(exc)
                message_type = "error"
            except Exception as exc:
                message = f"拼单完成失败：{exc}"
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
                group_order_id = parse_int(form_data["group_order_id"])
                if group_order_id is None:
                    raise ValueError("拼单编号不能为空")

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
                message = f"取消拼单失败：{exc}"
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
            message = f"查询失败：{exc}"
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
