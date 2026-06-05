from flask import Flask, render_template, request

from db import execute_write, fetch_one


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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
