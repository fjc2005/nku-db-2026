# P0报告指导

请结合 `docs/REPORT_TEMPLATE.md` 使用本指南。学号、姓名、专业等个人信息建议在最终提交前手动填写，不要在仓库文档中固定写入。

## 1. 项目信息

推荐填写内容：

| 报告项目 | 证据或取值 |
| --- | --- |
| 项目名称 | 校园奶茶拼单系统 |
| 所需环境 | Python、Flask、MySQL |
| 主要功能 | 拼单加入、完成、取消、明细查询 |
| 页面截图 | `/`、`/order/add`、`/group/finish`、`/group/cancel`、`/group/query` |

至少使用 3 张截图；更稳妥的截图组合是首页、添加订单、取消拼单和查询明细。

## 2. 系统配置

可用证据：

| 报告项目 | 来源 |
| --- | --- |
| Python 依赖 | `requirements.txt` |
| Flask 启动方式 | `README.md` |
| MySQL 表结构导入 | `schema.sql`、`README.md` |
| 数据库连接配置 | `db.py` |

连接参数分析：

| 参数名 | 作用 | 来源 |
| --- | --- | --- |
| `host` | MySQL 服务器地址 | `db.py` 中的 `DB_CONFIG` |
| `port` | MySQL 服务器端口 | `db.py` 中的 `DB_CONFIG` |
| `user` | MySQL 登录用户 | `db.py` 中的 `DB_CONFIG` |
| `password` | MySQL 登录密码 | `db.py` 中的 `DB_CONFIG` |
| `database` | 目标数据库名称 | `db.py` 中的 `DB_CONFIG` |
| `charset` | 客户端字符集 | `db.py` 中的 `DB_CONFIG` |
| `autocommit` | 事务自动提交开关 | `db.py` 中的 `DB_CONFIG` |

截图目标：`db.py` 中展示 `DB_CONFIG` 和 `get_connection()` 的代码。

## 3. 数据库设计

建表顺序：

| 顺序 | 表名 | 主键 | 参照属性 | 被参照表及属性 |
| --- | --- | --- | --- | --- |
| 1 | `students` | `student_id` | 无 | 无 |
| 2 | `shops` | `shop_id` | 无 | 无 |
| 3 | `drinks` | `drink_id` | `shop_id` | `shops(shop_id)` |
| 4 | `group_orders` | `group_order_id` | `shop_id`、`creator_student_id` | `shops(shop_id)`、`students(student_id)` |
| 5 | `coupons` | `coupon_id` | `student_id` | `students(student_id)` |
| 6 | `order_items` | `order_item_id` | `group_order_id`、`student_id`、`drink_id`、`coupon_id` | `group_orders(group_order_id)`、`students(student_id)`、`drinks(drink_id)`、`coupons(coupon_id)` |
| 7 | `operation_logs` | `log_id` | 无 | 无 |

截图目标：

- `schema.sql` 中的建表语句和外键约束。
- 通过 MySQL Workbench、Navicat 或 DBeaver 从 `milk_tea_group_db` 生成的数据库关系图。

## 4. 事务删除操作

报告填写值：

| 报告项目 | 内容 |
| --- | --- |
| 功能 | 取消未完成的拼单，恢复相关库存和优惠券，删除明细记录和主记录 |
| 相关表 | `group_orders`、`order_items`、`drinks`、`coupons`、`operation_logs` |
| 连接字段 | `order_items.group_order_id = group_orders.group_order_id` |
| 删除条件 | `group_orders.group_order_id = ?` |

截图目标：

- `app.py` 中的 `cancel_group_order_transaction` 函数。
- 以 `DELETE oi FROM order_items oi JOIN group_orders go` 开头的 SQL 代码块。
- `/group/cancel` 页面。

演示输入见 `docs/DEMO_CASES.md`。

## 5. 触发器控制的添加操作

报告填写值：

| 报告项目 | 内容 |
| --- | --- |
| 功能 | 向未完成的拼单中添加学生订单明细 |
| 触发器 | `trg_before_order_item_insert` 用于校验拼单状态、库存、店铺归属、优惠券状态，并计算金额 |
| 相关表 | `order_items`、`students`、`group_orders`、`drinks`、`coupons`、`operation_logs` |

输入规则：

| 字段 | 规则 |
| --- | --- |
| `group_order_id` | 必须引用状态为 `OPEN` 的拼单 |
| `student_id` | 必须引用状态为 `ACTIVE` 的学生 |
| `drink_id` | 必须引用同一店铺下状态为 `ON_SALE` 的饮品 |
| `quantity` | 必须大于 `0`，且不能超过库存 |
| `coupon_id` | 可选；如果填写，必须属于该学生，状态为 `UNUSED`，在有效期内，并满足最低使用金额 |

截图目标：

- `app.py` 中 `/order/add` 路由和参数化的 `INSERT INTO order_items` 语句。
- `schema.sql` 中的触发器 `trg_before_order_item_insert`。
- `/order/add` 页面的成功和失败提示。

演示输入见 `docs/DEMO_CASES.md`。

## 6. 存储过程更新操作

报告填写值：

| 报告项目 | 内容 |
| --- | --- |
| 功能 | 完成一个未完成的拼单 |
| 存储过程 | `sp_finish_group_order` 检查状态和明细记录，然后更新总金额和状态 |
| 相关表 | `group_orders`、`order_items`、`operation_logs` |
| 连接字段 | `group_orders.group_order_id = order_items.group_order_id` |

变化字段：

| 字段 | 规则 |
| --- | --- |
| `group_orders.total_amount` | 设置为 `SUM(order_items.pay_amount)` |
| `group_orders.status` | 设置为 `FINISHED` |
| `order_items.status` | 将该拼单下的明细状态设置为 `PAID` |

截图目标：

- `schema.sql` 中的存储过程 `sp_finish_group_order`。
- `app.py` 中展示 `callproc("sp_finish_group_order", ...)` 的 `finish_group_order` 函数。
- `/group/finish` 页面的成功和失败提示。

演示输入见 `docs/DEMO_CASES.md`。

## 7. 视图查询操作

报告填写值：

| 报告项目 | 内容 |
| --- | --- |
| 功能 | 按拼单编号、学生姓名或拼单状态查询拼单明细 |
| 视图 | `v_group_order_detail` 连接拼单、明细、学生、饮品和店铺信息 |
| 相关表 | `group_orders`、`order_items`、`students`、`drinks`、`shops` |
| 连接字段 | `group_orders.group_order_id = order_items.group_order_id`；`order_items.student_id = students.student_id`；`order_items.drink_id = drinks.drink_id`；`group_orders.shop_id = shops.shop_id` |

截图目标：

- `schema.sql` 中的视图 `v_group_order_detail`。
- `app.py` 中展示 `FROM v_group_order_detail` 的 `query_group_order_details` 函数。
- `/group/query` 页面中可见的表格查询结果。

演示输入见 `docs/DEMO_CASES.md`。

## 最终截图清单

- 首页 `/`
> 图片命名：`figs/01_homepage.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 激活环境：`source <conda_root>/etc/profile.d/conda.sh && conda activate db`。4. 如第一次运行或依赖有变化，安装依赖：`pip install -r requirements.txt`。5. 确认 MySQL 服务已启动。6. 重置演示数据库：`mysql -u <db_user> -p < schema.sql`，按提示输入数据库密码。7. 配置连接参数：`export DB_HOST=127.0.0.1`、`export DB_PORT=3306`、`export DB_USER=<db_user>`、`export DB_PASSWORD=<database_password>`、`export DB_NAME=milk_tea_group_db`、`export DB_CHARSET=utf8mb4`。8. 启动 Flask：`python app.py`，不要关闭该 Terminal。9. 打开浏览器访问 `http://127.0.0.1:5000/`。10. 确认首页能看到系统名称、四类评分操作入口和统计卡片后截图，保存为 `figs/01_homepage.png`。截图时不要把终端标题栏、用户名、绝对路径或密码截入图片。
- 添加订单 `/order/add`
> 图片命名：`figs/02_add_order_success.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 激活环境：`source <conda_root>/etc/profile.d/conda.sh && conda activate db`。4. 如第一次运行或依赖有变化，安装依赖：`pip install -r requirements.txt`。5. 确认 MySQL 服务已启动。6. 重置演示数据库：`mysql -u <db_user> -p < schema.sql`，按提示输入数据库密码。7. 配置连接参数：`export DB_HOST=127.0.0.1`、`export DB_PORT=3306`、`export DB_USER=<db_user>`、`export DB_PASSWORD=<database_password>`、`export DB_NAME=milk_tea_group_db`、`export DB_CHARSET=utf8mb4`。8. 启动 Flask：`python app.py`，不要关闭该 Terminal。9. 打开浏览器访问 `http://127.0.0.1:5000/order/add`。10. 表单中选择或填写：拼单 `1`、学生 `1`、饮品 `1`、数量 `1`、优惠券 `1`。11. 点击提交按钮。12. 确认页面显示“加入拼单成功”后截图，保存为 `figs/02_add_order_success.png`。截图时让成功提示和表单区域同时可见。
- 完成拼单 `/group/finish`
> 图片命名：`figs/03_finish_group_success.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 激活环境：`source <conda_root>/etc/profile.d/conda.sh && conda activate db`。4. 如第一次运行或依赖有变化，安装依赖：`pip install -r requirements.txt`。5. 确认 MySQL 服务已启动。6. 重置演示数据库：`mysql -u <db_user> -p < schema.sql`，按提示输入数据库密码。7. 配置连接参数：`export DB_HOST=127.0.0.1`、`export DB_PORT=3306`、`export DB_USER=<db_user>`、`export DB_PASSWORD=<database_password>`、`export DB_NAME=milk_tea_group_db`、`export DB_CHARSET=utf8mb4`。8. 启动 Flask：`python app.py`，不要关闭该 Terminal。9. 打开浏览器访问 `http://127.0.0.1:5000/group/finish`。10. 在拼单编号输入框填写 `2`。11. 点击提交按钮。12. 确认页面显示“拼单完成成功”后截图，保存为 `figs/03_finish_group_success.png`。截图时让成功提示和拼单编号输入框同时可见。
- 取消拼单 `/group/cancel`
> 图片命名：`figs/04_cancel_group_success.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 激活环境：`source <conda_root>/etc/profile.d/conda.sh && conda activate db`。4. 如第一次运行或依赖有变化，安装依赖：`pip install -r requirements.txt`。5. 确认 MySQL 服务已启动。6. 重置演示数据库：`mysql -u <db_user> -p < schema.sql`，按提示输入数据库密码。7. 配置连接参数：`export DB_HOST=127.0.0.1`、`export DB_PORT=3306`、`export DB_USER=<db_user>`、`export DB_PASSWORD=<database_password>`、`export DB_NAME=milk_tea_group_db`、`export DB_CHARSET=utf8mb4`。8. 启动 Flask：`python app.py`，不要关闭该 Terminal。9. 打开浏览器访问 `http://127.0.0.1:5000/group/cancel`。10. 在拼单编号输入框填写 `5`。11. 点击提交按钮。12. 确认页面显示“取消拼单成功”，并显示删除明细、恢复饮品、恢复优惠券数量后截图，保存为 `figs/04_cancel_group_success.png`。截图时让成功提示和输入框同时可见。
- 查询拼单明细 `/group/query`
> 图片命名：`figs/05_query_group_detail.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 激活环境：`source <conda_root>/etc/profile.d/conda.sh && conda activate db`。4. 如第一次运行或依赖有变化，安装依赖：`pip install -r requirements.txt`。5. 确认 MySQL 服务已启动。6. 重置演示数据库：`mysql -u <db_user> -p < schema.sql`，按提示输入数据库密码。7. 配置连接参数：`export DB_HOST=127.0.0.1`、`export DB_PORT=3306`、`export DB_USER=<db_user>`、`export DB_PASSWORD=<database_password>`、`export DB_NAME=milk_tea_group_db`、`export DB_CHARSET=utf8mb4`。8. 启动 Flask：`python app.py`，不要关闭该 Terminal。9. 打开浏览器访问 `http://127.0.0.1:5000/group/query`。10. 在拼单编号输入框填写 `3`，拼单状态选择 `FINISHED`，学生姓名保持为空。11. 点击查询按钮。12. 确认可见拼单、学生、店铺、饮品、金额等表格结果后截图，保存为 `figs/05_query_group_detail.png`。
- `db.py` 中的连接代码
> 图片命名：`figs/06_db_connection_code.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 打开连接代码位置：`code -g db.py:1`；如果没有 `code` 命令，用任意代码编辑器打开 `db.py`。4. 让截图画面中清晰显示 `DB_CONFIG`、环境变量读取和 `get_connection()`。5. 截图并保存为 `figs/06_db_connection_code.png`。如果只能截 Terminal，运行 `nl -ba db.py | sed -n '1,18p'`，只截代码输出区域，不截用户名、绝对路径或窗口标题栏。
- `app.py` 中的事务代码
> 图片命名：`figs/07_transaction_delete_code.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 打开事务代码位置：`code -g app.py:181`；如果没有 `code` 命令，用任意代码编辑器打开 `app.py` 并搜索 `cancel_group_order_transaction`。4. 让截图画面中清晰显示 `connection.start_transaction()`、`DELETE oi FROM order_items oi JOIN group_orders go`、`connection.commit()` 或 `connection.rollback()`。5. 截图并保存为 `figs/07_transaction_delete_code.png`。如果只能截 Terminal，运行 `nl -ba app.py | sed -n '181,295p'`，只截关键代码输出区域。
- `schema.sql` 中的触发器代码
> 图片命名：`figs/08_trigger_code.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 打开触发器代码位置：`code -g schema.sql:186`；如果没有 `code` 命令，用任意代码编辑器打开 `schema.sql` 并搜索 `CREATE TRIGGER trg_before_order_item_insert`。4. 让截图画面中清晰显示 `CREATE TRIGGER trg_before_order_item_insert`、`BEFORE INSERT ON order_items`、`SIGNAL SQLSTATE` 校验逻辑，以及扣库存或更新优惠券状态的 SQL。5. 截图并保存为 `figs/08_trigger_code.png`。如果只能截 Terminal，运行 `nl -ba schema.sql | sed -n '186,335p'`，滚动到能同时看见触发器名称和核心校验代码的位置再截图。
- `schema.sql` 中的存储过程代码
> 图片命名：`figs/09_stored_procedure_code.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 打开存储过程代码位置：`code -g schema.sql:379`；如果没有 `code` 命令，用任意代码编辑器打开 `schema.sql` 并搜索 `CREATE PROCEDURE sp_finish_group_order`。4. 让截图画面中清晰显示 `CREATE PROCEDURE sp_finish_group_order`、状态校验、`UPDATE group_orders` 和 `UPDATE order_items`。5. 截图并保存为 `figs/09_stored_procedure_code.png`。如果只能截 Terminal，运行 `nl -ba schema.sql | sed -n '379,440p'`，只截关键代码输出区域。
- `schema.sql` 中的视图代码
> 图片命名：`figs/10_view_code.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 打开视图代码位置：`code -g schema.sql:348`；如果没有 `code` 命令，用任意代码编辑器打开 `schema.sql` 并搜索 `CREATE VIEW v_group_order_detail`。4. 让截图画面中清晰显示 `CREATE VIEW v_group_order_detail`、`FROM group_orders go`，以及连接 `order_items`、`students`、`drinks`、`shops` 的 `JOIN` 语句。5. 截图并保存为 `figs/10_view_code.png`。如果只能截 Terminal，运行 `nl -ba schema.sql | sed -n '348,377p'`，只截代码输出区域。
- 通过 MySQL 图形化工具生成的数据库关系图
> 图片命名：`figs/11_database_relationship_diagram.png`。操作流程：1. 打开 Terminal，进入项目目录：`cd <project_root>`。2. 准备截图目录：`mkdir -p figs`。3. 确认 MySQL 服务已启动。4. 重置演示数据库：`mysql -u <db_user> -p < schema.sql`，按提示输入数据库密码。5. 打开 MySQL Workbench、Navicat 或 DBeaver。6. 新建或选择 MySQL 连接，主机填 `127.0.0.1`，端口填 `3306`，用户填 `<db_user>`，密码填你的数据库密码。7. 连接后选择数据库 `milk_tea_group_db`。8. 如果使用 MySQL Workbench，点击 `Database` -> `Reverse Engineer`，选择该连接和 `milk_tea_group_db`，一路点击 `Next` 到生成 EER Diagram；如果使用 DBeaver，右键数据库或表区域，选择生成/查看 ER Diagram；如果使用 Navicat，进入数据库后使用图表/ER 图功能生成关系图。9. 调整缩放，让 `students`、`shops`、`drinks`、`group_orders`、`coupons`、`order_items`、`operation_logs` 及外键连线尽量可见。10. 截图并保存为 `figs/11_database_relationship_diagram.png`。截图时不要包含连接配置窗口里的密码。

# P0 Report Evidence Guide

Use this guide together with `docs/REPORT_TEMPLATE.md`. Keep personal fields such
as student number, name, and major as manual placeholders until final submission.

## 1. Project Information

Recommended values:

| Report item | Evidence or value |
| --- | --- |
| Project name | 校园奶茶拼单系统 |
| Required environment | Python, Flask, MySQL |
| Main functions | Group order join, finish, cancel, and detail query |
| Page screenshots | `/`, `/order/add`, `/group/finish`, `/group/cancel`, `/group/query` |

Use at least 3 screenshots; the safest set is homepage, add order, cancel group,
and query detail.

## 2. System Configuration

Evidence:

| Report item | Source |
| --- | --- |
| Python dependencies | `requirements.txt` |
| Flask startup | `README.md` |
| MySQL schema import | `schema.sql`, `README.md` |
| Connection configuration | `db.py` |

Connection parameter analysis:

| Name | Purpose | Source |
| --- | --- | --- |
| `host` | MySQL server address | `DB_CONFIG` in `db.py` |
| `port` | MySQL server port | `DB_CONFIG` in `db.py` |
| `user` | MySQL login user | `DB_CONFIG` in `db.py` |
| `password` | MySQL login password | `DB_CONFIG` in `db.py` |
| `database` | Target database name | `DB_CONFIG` in `db.py` |
| `charset` | Client character set | `DB_CONFIG` in `db.py` |
| `autocommit` | Transaction auto-commit switch | `DB_CONFIG` in `db.py` |

Screenshot target: `db.py` showing `DB_CONFIG` and `get_connection()`.

## 3. Database Design

Table creation order:

| Order | Table | Primary key | Reference attributes | Referenced table and attributes |
| --- | --- | --- | --- | --- |
| 1 | `students` | `student_id` | None | None |
| 2 | `shops` | `shop_id` | None | None |
| 3 | `drinks` | `drink_id` | `shop_id` | `shops(shop_id)` |
| 4 | `group_orders` | `group_order_id` | `shop_id`, `creator_student_id` | `shops(shop_id)`, `students(student_id)` |
| 5 | `coupons` | `coupon_id` | `student_id` | `students(student_id)` |
| 6 | `order_items` | `order_item_id` | `group_order_id`, `student_id`, `drink_id`, `coupon_id` | `group_orders(group_order_id)`, `students(student_id)`, `drinks(drink_id)`, `coupons(coupon_id)` |
| 7 | `operation_logs` | `log_id` | None | None |

Screenshot targets:

- `schema.sql` table definitions and foreign key constraints.
- MySQL Workbench, Navicat, or DBeaver relationship diagram generated from `milk_tea_group_db`.

## 4. Transaction Delete Operation

Report values:

| Report item | Value |
| --- | --- |
| Function | Cancel an open group order, restore related stock and coupons, delete details and master record |
| Related tables | `group_orders`, `order_items`, `drinks`, `coupons`, `operation_logs` |
| Join field | `order_items.group_order_id = group_orders.group_order_id` |
| Delete condition | `group_orders.group_order_id = ?` |

Screenshot targets:

- `app.py` function `cancel_group_order_transaction`.
- SQL block beginning with `DELETE oi FROM order_items oi JOIN group_orders go`.
- Page `/group/cancel`.

Demo inputs are in `docs/DEMO_CASES.md`.

## 5. Trigger-Controlled Add Operation

Report values:

| Report item | Value |
| --- | --- |
| Function | Add a student order item to an open group order |
| Trigger | `trg_before_order_item_insert` validates status, stock, shop ownership, coupon state, and calculates amounts |
| Related tables | `order_items`, `students`, `group_orders`, `drinks`, `coupons`, `operation_logs` |

Input rules:

| Field | Rule |
| --- | --- |
| `group_order_id` | Must reference an `OPEN` group order |
| `student_id` | Must reference an `ACTIVE` student |
| `drink_id` | Must reference an `ON_SALE` drink in the same shop |
| `quantity` | Must be greater than `0` and not exceed stock |
| `coupon_id` | Optional; if present, must belong to the student, be `UNUSED`, valid, and meet the minimum amount |

Screenshot targets:

- `app.py` route `/order/add` and the parameterized `INSERT INTO order_items`.
- `schema.sql` trigger `trg_before_order_item_insert`.
- Page `/order/add` success and failure messages.

Demo inputs are in `docs/DEMO_CASES.md`.

## 6. Stored Procedure Update Operation

Report values:

| Report item | Value |
| --- | --- |
| Function | Finish an open group order |
| Stored procedure | `sp_finish_group_order` checks state and details, then updates total amount and statuses |
| Related tables | `group_orders`, `order_items`, `operation_logs` |
| Join field | `group_orders.group_order_id = order_items.group_order_id` |

Changed fields:

| Field | Rule |
| --- | --- |
| `group_orders.total_amount` | Set to `SUM(order_items.pay_amount)` |
| `group_orders.status` | Set to `FINISHED` |
| `order_items.status` | Set to `PAID` for the finished group |

Screenshot targets:

- `schema.sql` procedure `sp_finish_group_order`.
- `app.py` function `finish_group_order` showing `callproc("sp_finish_group_order", ...)`.
- Page `/group/finish` success and failure messages.

Demo inputs are in `docs/DEMO_CASES.md`.

## 7. View Query Operation

Report values:

| Report item | Value |
| --- | --- |
| Function | Query group order details by group id, student name, or group status |
| View | `v_group_order_detail` joins group, item, student, drink, and shop details |
| Related tables | `group_orders`, `order_items`, `students`, `drinks`, `shops` |
| Join fields | `group_orders.group_order_id = order_items.group_order_id`; `order_items.student_id = students.student_id`; `order_items.drink_id = drinks.drink_id`; `group_orders.shop_id = shops.shop_id` |

Screenshot targets:

- `schema.sql` view `v_group_order_detail`.
- `app.py` function `query_group_order_details` showing `FROM v_group_order_detail`.
- Page `/group/query` with visible table results.

Demo inputs are in `docs/DEMO_CASES.md`.

## Final Screenshot Checklist

- Homepage `/`
- Add order `/order/add`
- Finish group order `/group/finish`
- Cancel group order `/group/cancel`
- Query group detail `/group/query`
- Connection code in `db.py`
- Transaction code in `app.py`
- Trigger code in `schema.sql`
- Stored procedure code in `schema.sql`
- View code in `schema.sql`
- Database relationship diagram from a MySQL GUI tool
