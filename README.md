# 校园奶茶拼单系统

这是一个基于 Flask + MySQL 的 P0/P1 数据库工程演示系统，用于展示校园奶茶拼单的核心数据库操作流程和演示辅助页面。

## 包含内容

- Flask Web 应用：`app.py`
- MySQL 连接封装：`db.py`
- 数据库重置和对象脚本：`schema.sql`
- HTML 模板：`templates/`
- CSS 样式：`static/style.css`
- 演示用例说明：`docs/DEMO_CASES.md`

## 运行环境

- 使用 conda 管理 Python 环境
- MySQL 8.0 或兼容的 MySQL 服务
- Python 依赖见 `requirements.txt`

你可以通过以下命令创建 conda 环境:

```bash
conda create -n db python=3.12 -y
conda activate db
```

随后使用 pip 安装必要依赖：

```bash
pip install -r requirements.txt
```

## 数据库初始化

使用 MySQL 客户端执行 `schema.sql`，创建或重置数据库：

```bash
mysql -u <db_user> -p < schema.sql
```

该脚本会重建 `milk_tea_group_db`，并创建 P0/P1 所需的数据表、演示数据、触发器、存储过程、视图和操作日志基础数据。

## 数据库连接配置

`db.py` 读取以下环境变量；未设置时使用本地默认值：

| 变量 | 含义 | 默认值 |
| --- | --- | --- |
| `DB_HOST` | MySQL 主机 | `127.0.0.1` |
| `DB_PORT` | MySQL 端口 | `3306` |
| `DB_USER` | MySQL 用户 | `root` |
| `DB_PASSWORD` | MySQL 密码 | 空字符串 |
| `DB_NAME` | 数据库名称 | `milk_tea_group_db` |
| `DB_CHARSET` | 客户端字符集 | `utf8mb4` |

配置示例：

```bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=<db_user>
export DB_PASSWORD=<database_password>
export DB_NAME=milk_tea_group_db
export DB_CHARSET=utf8mb4
```

`db.py` 中的 `autocommit` 设置为 `False`，用于支持事务演示。

## 启动应用

```bash
python app.py
```

浏览器访问：

```text
http://127.0.0.1:5000
```

如果 `5000` 端口已被占用，可以用其他端口启动：

```bash
python -c "from app import app; app.run(host='127.0.0.1', port=5001, debug=True)"
```

## P0 页面

| 页面 | 路径 | 用途 |
| --- | --- | --- |
| 首页 | `/` | 展示系统名称、数据库统计和 P0 入口 |
| 加入拼单 | `/order/add` | 演示由触发器控制的插入操作 |
| 完成拼单 | `/group/finish` | 演示由存储过程控制的更新操作 |
| 取消拼单 | `/group/cancel` | 演示显式事务删除操作 |
| 查询拼单详情 | `/group/query` | 演示基于视图的多表查询 |

## P1 页面

| 页面 | 路径 | 用途 |
| --- | --- | --- |
| 学生列表 | `/data/students` | 查看学生编号、姓名、手机号和状态 |
| 店铺列表 | `/data/shops` | 查看店铺名称、校区位置和状态 |
| 饮品列表 | `/data/drinks` | 查看饮品价格、库存和状态变化 |
| 优惠券列表 | `/data/coupons` | 查看优惠券金额、有效期和使用状态 |
| 操作日志 | `/logs` | 查看加入、完成和取消拼单的关键操作日志 |

## 演示输入

推荐输入值、P1 演示路线和预期结果见 `docs/DEMO_CASES.md`。重复执行取消拼单等破坏性演示前，建议重新执行 `schema.sql` 重置数据库。

## 常见问题

- 首页提示数据库不可用：启动 MySQL，导入 `schema.sql`，并检查 `DB_*` 环境变量。
- MySQL 导入已有数据库失败：`schema.sql` 会先删除再重建 `milk_tea_group_db`，请确认 MySQL 用户有相应权限。
- 存储过程或触发器文本显示异常：确认 MySQL 客户端使用 `utf8mb4`。
- `5000` 端口被占用：使用上方备用端口启动命令。

# Campus Milk Tea Group Ordering System

This is a P0/P1 Flask + MySQL database engineering demo system for the core workflows and demo helper pages of a campus milk tea group-ordering scenario.

## What Is Included

- Flask web app: `app.py`
- MySQL connection helper: `db.py`
- Database reset and object script: `schema.sql`
- HTML templates: `templates/`
- CSS: `static/style.css`
- Demo walkthrough: `docs/DEMO_CASES.md`

## Environment

- Python managed by conda
- MySQL 8.0 or a compatible MySQL server
- Python packages listed in `requirements.txt`

You can use following command to build up conda environment:

```bash
conda create -n db python=3.12 -y
conda activate db
```

And then, you should use `pip` to install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Create or reset the database by executing `schema.sql` with a MySQL client:

```bash
mysql -u <db_user> -p < schema.sql
```

The script recreates `milk_tea_group_db`, creates all P0/P1 tables, seed data, trigger, stored procedure, view, and operation log seed data.

## Connection Configuration

`db.py` reads these environment variables and falls back to local defaults:

| Variable | Meaning | Default |
| --- | --- | --- |
| `DB_HOST` | MySQL host | `127.0.0.1` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `root` |
| `DB_PASSWORD` | MySQL password | empty string |
| `DB_NAME` | Database name | `milk_tea_group_db` |
| `DB_CHARSET` | Client character set | `utf8mb4` |

Example:

```bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=<db_user>
export DB_PASSWORD=<database_password>
export DB_NAME=milk_tea_group_db
export DB_CHARSET=utf8mb4
```

`autocommit` is set to `False` in `db.py` for transaction demos.

## Run The App

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

If port `5000` is already in use, start the app on another port:

```bash
python -c "from app import app; app.run(host='127.0.0.1', port=5001, debug=True)"
```

## P0 Pages

| Page | Path | Purpose |
| --- | --- | --- |
| Homepage | `/` | System name, database statistics, and P0 entrances |
| Add order | `/order/add` | Trigger-controlled insert |
| Finish group order | `/group/finish` | Stored-procedure-controlled update |
| Cancel group order | `/group/cancel` | Explicit transaction delete |
| Query group detail | `/group/query` | View-based multi-table query |

## P1 Pages

| Page | Path | Purpose |
| --- | --- | --- |
| Students | `/data/students` | View student number, name, phone, and status |
| Shops | `/data/shops` | View shop name, campus location, and status |
| Drinks | `/data/drinks` | View drink price, inventory, and status changes |
| Coupons | `/data/coupons` | View coupon amount, validity date, and usage status |
| Operation logs | `/logs` | View key add, finish, and cancel operation logs |

## Demo Inputs

Use `docs/DEMO_CASES.md` for the recommended input values, P1 demo route, and expected results. Re-run `schema.sql` before repeating a destructive demo such as canceling a group order.

## Common Issues

- Homepage shows database unavailable: start MySQL, import `schema.sql`, and check `DB_*` variables.
- MySQL import fails on an existing database: `schema.sql` already drops and recreates `milk_tea_group_db`; confirm the MySQL user has permission.
- Stored procedure or trigger text displays incorrectly: confirm the MySQL client uses `utf8mb4`.
- Port `5000` is busy: run the alternate port command shown above.
