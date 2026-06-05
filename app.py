from flask import Flask, render_template

from db import fetch_one


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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
