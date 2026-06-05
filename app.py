from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        stats = [
            {"label": "学生数", "value": "--", "status": "待接入数据库"},
            {"label": "饮品数", "value": "--", "status": "待接入数据库"},
            {"label": "进行中拼单", "value": "--", "status": "待接入数据库"},
        ]
        return render_template("index.html", stats=stats)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
