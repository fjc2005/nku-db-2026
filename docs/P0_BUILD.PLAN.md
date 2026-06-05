# P0 分 Stage 搭建计划

本文档用于指导“校园奶茶拼单系统”P0 范围的逐 stage 实施。每个 stage 都必须形成 `plan -> develop -> verify -> commit` 闭环；只有当前 stage 已验证并提交后，才开始下一个 stage。

## 0. 执行约定

1. 每个 stage 开始前，先确认本 stage 的目标、涉及文件、覆盖的 P0 条目和验收方式。
2. 每个 stage 的代码开发必须尽量小步提交，避免把多个评分点混在一个提交中。
3. 每个 stage 完成后必须执行本 stage 的 verify 清单；未通过时先修复，不进入 commit。
4. Commit title 使用 `<action>: <message>` 格式；`action` 优先使用 `update`、`fix`、`delete`、`doc`，其他动作仅在更贴合变更时使用。
5. 每个 commit 除标题外必须包含详细描述正文，说明本次变更内容、验证结果和影响范围。
6. 文档、配置示例和 README 不写入本机绝对路径、真实用户名、设备信息或真实数据库密码。
7. 运行 Python 或 Flask 前先激活项目约定的 conda 环境；依赖变更必须同步更新 `requirements.txt`。
8. Python SQL 操作必须使用参数化查询；事务失败必须 rollback；数据库连接和 cursor 必须关闭。
9. P0 阶段不实现登录权限系统，页面入口模拟学生、发起人和管理员操作。

## 1. P0 范围摘要

P0 必须交付一个可运行的 Flask + MySQL 小型 B/S 系统，满足数据库工程作业评分点：

1. 独立 MySQL 数据库 `milk_tea_group_db`。
2. 7 张业务表：`students`、`shops`、`drinks`、`group_orders`、`coupons`、`order_items`、`operation_logs`。
3. 外键关系、初始化演示数据、触发器、存储过程、视图均在 `schema.sql` 中创建。
4. Python 通过 `mysql-connector-python` 连接 MySQL，统一使用 `get_connection()`。
5. 5 个 P0 页面：`/`、`/order/add`、`/group/finish`、`/group/cancel`、`/group/query`。
6. 加入拼单演示触发器控制下的添加操作。
7. 完成拼单演示存储过程控制下的更新操作。
8. 取消拼单演示显式事务控制下的删除操作。
9. 拼单详情演示基于视图的多表查询操作。
10. README、报告素材和截图清单能够支撑课程报告填写与现场演示。

## 2. Stage Gate 模板

每个 stage 必须按以下格式执行：

| 步骤 | 要求 |
| --- | --- |
| Plan | 明确本 stage 目标、涉及 P0 编号、改动文件、风险和验收命令。 |
| Develop | 只实现本 stage 范围内的文件改动，不提前实现后续 stage。 |
| Verify | 执行本 stage 的最小可验证检查，并记录结果。 |
| Commit | 验证通过后提交；提交标题使用 `<action>: <message>`；提交正文写清变更内容、验证结果和影响范围；提交后再次确认工作区只剩用户允许保留的变更。 |

Commit 正文建议模板：

```text
Changes:
- <本 stage 的主要变更>

Verification:
- <已执行的验证步骤和结果>

Scope:
- <影响范围或未覆盖事项>
```

## 3. 分 Stage 计划

### Stage 00：P0 搭建计划基线

覆盖需求：项目推进约定、P0 范围拆分。

Plan：

1. 阅读 `docs/REQUIREMENT.md`，提取 P0 必须项、页面清单、数据库对象清单、演示数据要求和最终交付物。
2. 设计后续 stage，使每个 stage 都有明确可验证成果和提交边界。
3. 确认计划文档不包含本机绝对路径、真实凭据或用户设备信息。

Develop：

1. 新增 `docs/P0_BUILD.PLAN.md`。
2. 写入全局执行约定、P0 摘要、stage gate 和逐 stage 实施计划。

Verify：

1. 检查文档存在且 Markdown 可读。
2. 检查文档仅使用相对路径和占位符。
3. 检查每个 stage 都包含 Plan、Develop、Verify、Commit。

Commit：

1. 提交标题：`doc: add P0 staged build plan`。
2. 提交描述：说明新增 P0 分 stage 搭建计划、已验证闭环结构和敏感信息检查结果。

### Stage 01：项目骨架与依赖基线

覆盖需求：NF-001、NF-002、NF-003 的基础部分。

Plan：

1. 建立推荐目录结构，先让 Flask 应用可以启动。
2. 不连接数据库，不实现业务逻辑，只交付最小页面和依赖文件。
3. 明确后续数据库配置文件放置位置。

Develop：

1. 新增 `app.py`、`requirements.txt`、`templates/base.html`、`templates/index.html`、`static/style.css`。
2. 在 `requirements.txt` 中加入 `flask` 和 `mysql-connector-python`。
3. 首页先展示项目名称和占位统计，后续 stage 再接入真实数据库。

Verify：

1. 激活 conda 环境后安装依赖：`pip install -r requirements.txt`。
2. 启动 Flask：`python app.py`。
3. 访问 `http://127.0.0.1:5000`，确认首页可打开并显示“校园奶茶拼单系统”。

Commit：

1. 提交标题：`update: add flask project skeleton`。
2. 提交描述：说明新增 Flask 骨架、依赖和基础页面，以及本 stage 的启动验证结果。

### Stage 02：数据库基础表与演示种子数据

覆盖需求：P0-DB-001 至 P0-DB-011 中的表、外键和基础数据部分。

Plan：

1. 设计 `schema.sql` 的建库、建表、外键和初始化数据顺序。
2. 表创建顺序按报告要求保持清晰：`students`、`shops`、`drinks`、`group_orders`、`coupons`、`order_items`、`operation_logs`。
3. 种子数据需要覆盖 ACTIVE/LOCKED 学生、OPEN/FINISHED/CANCELED 拼单、UNUSED/USED 优惠券、库存充足和失败案例。

Develop：

1. 新增 `schema.sql`，创建数据库 `milk_tea_group_db`。
2. 创建 7 张业务表，补齐主键、唯一约束、CHECK 约束和外键约束。
3. 插入最小演示数据：至少 3 名学生、2 家店铺、5 个饮品、2 个拼单、3 张优惠券，并预留后续演示数据。

Verify：

1. 使用 MySQL 执行 `schema.sql`。
2. 查询数据库和表是否存在。
3. 查询每张表的记录数、外键约束和关键状态枚举数据。
4. 确认 `schema.sql` 可以重复执行或在清库后重新执行。

Commit：

1. 提交标题：`update: add mysql schema and seed data`。
2. 提交描述：说明新增数据库、业务表、外键和种子数据，以及 schema 导入验证结果。

### Stage 03：数据库连接封装

覆盖需求：P0-CONN-001、P0-CONN-002、P0-CONN-003、NF-004、NF-006。

Plan：

1. 建立统一数据库配置和连接方法。
2. 配置项必须包含 `host`、`port`、`user`、`password`、`database`、`charset`、`autocommit`。
3. 默认 `autocommit` 设为 `False`，便于事务演示。

Develop：

1. 新增 `db.py`，实现 `DB_CONFIG` 和 `get_connection()`。
2. 所有连接参数集中在 `db.py`，密码使用占位默认值或环境变量覆盖。
3. 为后续路由准备通用查询辅助函数，确保 cursor 和 connection 可关闭。

Verify：

1. 激活 conda 环境后运行一个最小连接检查脚本或临时 Flask 路由。
2. 确认能读取 `students`、`drinks`、`group_orders` 基础数据。
3. 确认连接代码中 `autocommit=False`，且未重复硬编码连接参数。

Commit：

1. 提交标题：`update: add mysql connection helper`。
2. 提交描述：说明新增统一连接封装、连接参数来源和数据库读取验证结果。

### Stage 04：首页真实统计接入

覆盖需求：P0-UI-001、P1-DEMO-001 的 P0 可用入口部分、P1-DEMO-002 的基础统计部分。

Plan：

1. 首页统计从 MySQL 读取真实数据。
2. 首页提供 4 个 P0 操作入口：加入拼单、完成拼单、取消拼单、拼单详情查询。
3. 页面保持简单清晰，优先支撑截图和演示。

Develop：

1. 更新 `app.py` 首页路由，读取学生数量、饮品数量、进行中拼单数量。
2. 更新 `templates/index.html` 展示统计和 P0 页面入口。
3. 补充基础错误提示，数据库不可用时页面不暴露堆栈。

Verify：

1. 启动 Flask，访问 `/`。
2. 确认首页显示项目名称和 3 个真实统计值。
3. 修改或查询数据库记录后，确认统计值能反映数据库状态。

Commit：

1. 提交标题：`update: connect homepage statistics`。
2. 提交描述：说明首页统计接入数据库、入口展示变更和页面验证结果。

### Stage 05：订单插入触发器

覆盖需求：P0-TRG-001 至 P0-TRG-015，P0-DB-011 的触发器部分。

Plan：

1. 在 `schema.sql` 中实现 `trg_before_order_item_insert`。
2. 触发器必须覆盖学生、拼单、饮品、数量、库存、优惠券归属、状态、有效期和金额计算。
3. 成功插入时扣减库存、更新优惠券状态；失败时数据库报明确错误。

Develop：

1. 修改 `schema.sql`，创建 `BEFORE INSERT` 触发器。
2. 在触发器中计算 `item_amount`、`discount_amount`、`pay_amount`。
3. 补充或调整演示数据，保证有成功和失败案例。

Verify：

1. 重建数据库。
2. 执行合法 `INSERT INTO order_items ...`，确认订单新增、金额正确、库存扣减、优惠券变为 `USED`。
3. 执行非法插入，例如 LOCKED 学生或库存不足，确认插入失败且库存和优惠券不变。
4. 确认触发器源码可截图。

Commit：

1. 提交标题：`update: add order insert trigger`。
2. 提交描述：说明触发器规则、演示数据调整和成功失败 SQL 验证结果。

### Stage 06：加入拼单页面与后端

覆盖需求：P0-UI-002、P0-TRG-014、P0-TRG-015、NF-006。

Plan：

1. 页面路径固定为 `/order/add`。
2. 表单使用编号输入，满足 P0；暂不强制做下拉框。
3. 提交时只插入必要字段，金额由触发器自动计算。

Develop：

1. 在 `app.py` 中新增 `/order/add` GET/POST 路由。
2. 新增 `templates/add_order.html`。
3. 使用参数化 SQL 插入 `order_items`。
4. 页面显示成功或数据库错误信息。

Verify：

1. 打开 `/order/add`，确认表单项包含拼单编号、学生编号、饮品编号、数量、优惠券编号。
2. 提交合法数据，确认页面提示“加入拼单成功”。
3. 提交非法数据，确认页面显示数据库错误信息且无脏数据。
4. 检查源码截图点：Python 插入代码和触发器 SQL 均可定位。

Commit：

1. 提交标题：`update: add group order join page`。
2. 提交描述：说明加入拼单页面、参数化插入逻辑和触发器页面演示结果。

### Stage 07：完成拼单存储过程

覆盖需求：P0-SP-001 至 P0-SP-011，P0-DB-011 的存储过程部分。

Plan：

1. 在 `schema.sql` 中创建 `sp_finish_group_order(p_group_order_id)`。
2. 存储过程检查拼单存在、状态为 `OPEN`、至少有一条订单明细。
3. 存储过程更新 `group_orders.total_amount`、`group_orders.status`、`order_items.status`。

Develop：

1. 修改 `schema.sql`，新增存储过程。
2. 补齐成功演示拼单和重复完成失败案例。
3. 确保存储过程涉及 `group_orders` 和 `order_items` 两张关系表。

Verify：

1. 重建数据库。
2. 调用存储过程完成一个 `OPEN` 且有明细的拼单。
3. 查询拼单状态、明细状态、总金额是否正确。
4. 重复调用同一拼单，确认失败并返回明确错误。
5. 确认存储过程源码可截图。

Commit：

1. 提交标题：`update: add finish group order procedure`。
2. 提交描述：说明完成拼单存储过程、状态和金额更新规则，以及调用验证结果。

### Stage 08：完成拼单页面与 Python 调用

覆盖需求：P0-UI-003、P0-SP-009、P0-SP-010、P0-SP-011。

Plan：

1. 页面路径固定为 `/group/finish`。
2. 后端必须通过 Python 调用 `sp_finish_group_order`。
3. 页面展示成功和失败提示。

Develop：

1. 在 `app.py` 中新增 `/group/finish` GET/POST 路由。
2. 新增 `templates/finish_group.html`。
3. 使用 `callproc("sp_finish_group_order", ...)` 或等价调用，并正确 commit/rollback。

Verify：

1. 打开 `/group/finish`，确认有拼单编号输入项。
2. 提交可完成拼单，确认提示“拼单完成成功”。
3. 重复提交同一拼单或提交不存在编号，确认失败提示。
4. 查询数据库确认状态、金额和明细状态符合预期。

Commit：

1. 提交标题：`update: add finish group order page`。
2. 提交描述：说明完成拼单页面、Python 存储过程调用和成功失败页面验证结果。

### Stage 09：取消拼单事务服务

覆盖需求：P0-TX-001 至 P0-TX-011、NF-005、NF-006。

Plan：

1. 在 Python 中实现显式事务取消拼单，不放入存储过程。
2. 事务内检查拼单存在且状态为 `OPEN`。
3. 恢复库存、恢复优惠券、使用 JOIN 删除订单明细、删除拼单主记录。

Develop：

1. 在 `app.py` 或后续业务模块中新增取消拼单函数。
2. 使用 `start_transaction()`、`commit()`、`rollback()`。
3. 删除订单明细 SQL 必须体现 `JOIN`。
4. 所有用户输入使用参数化查询。

Verify：

1. 对可取消的 `OPEN` 拼单执行取消函数。
2. 确认库存恢复、优惠券恢复、订单明细删除、拼单主记录删除。
3. 对 `FINISHED` 拼单执行取消，确认事务回滚且数据不变。
4. 检查事务源码可截图。

Commit：

1. 提交标题：`update: add cancel group order transaction`。
2. 提交描述：说明取消拼单事务、库存和优惠券恢复、JOIN 删除以及回滚验证结果。

### Stage 10：取消拼单页面

覆盖需求：P0-UI-004、P0-TX-010、P0-TX-011。

Plan：

1. 页面路径固定为 `/group/cancel`。
2. 页面只承担输入、调用事务函数和显示结果。
3. 成功和失败演示都通过页面完成。

Develop：

1. 在 `app.py` 中新增 `/group/cancel` GET/POST 路由。
2. 新增 `templates/cancel_group.html`。
3. 页面展示取消成功、拼单不存在、状态不允许取消等提示。

Verify：

1. 打开 `/group/cancel`，确认有拼单编号输入项。
2. 提交可取消拼单，确认提示“取消拼单成功”。
3. 提交已完成拼单，确认失败提示且数据库数据不变。
4. 确认页面截图和事务代码截图点都可定位。

Commit：

1. 提交标题：`update: add cancel group order page`。
2. 提交描述：说明取消拼单页面、事务函数调用和成功失败演示结果。

### Stage 11：拼单详情视图

覆盖需求：P0-VIEW-001 至 P0-VIEW-011，P0-DB-011 的视图部分。

Plan：

1. 在 `schema.sql` 中创建 `v_group_order_detail`。
2. 视图整合学生、店铺、饮品、拼单和订单明细信息。
3. 视图连接字段必须能直接对应报告要求。

Develop：

1. 修改 `schema.sql`，新增视图。
2. 视图字段包含学生姓名、学号、店铺名称、饮品名称、单价、拼单标题、拼单状态、总金额、数量、原价、优惠、实付和明细状态。
3. 补齐至少一条完整可查询演示数据。

Verify：

1. 重建数据库。
2. 直接查询 `v_group_order_detail`。
3. 验证按拼单编号、学生姓名、拼单状态筛选时结果正确。
4. 确认视图源码可截图。

Commit：

1. 提交标题：`update: add group order detail view`。
2. 提交描述：说明详情视图字段、表连接关系和视图查询验证结果。

### Stage 12：拼单详情查询页面

覆盖需求：P0-UI-005、P0-VIEW-008、P0-VIEW-009、P0-VIEW-010、P0-VIEW-011。

Plan：

1. 页面路径固定为 `/group/query`。
2. 查询必须只从 `v_group_order_detail` 读取。
3. 支持拼单编号、学生姓名模糊查询、拼单状态筛选。

Develop：

1. 在 `app.py` 中新增 `/group/query` GET 路由。
2. 新增 `templates/query_group.html`。
3. 使用参数化 SQL 动态组合 WHERE 条件，避免拼接用户输入。
4. 查询结果使用表格展示。

Verify：

1. 打开 `/group/query`，确认有三个筛选项。
2. 不输入条件时显示全部或默认结果。
3. 分别按拼单编号、学生姓名、状态查询，确认结果来自视图且筛选正确。
4. 确认查询代码和视图代码可截图。

Commit：

1. 提交标题：`update: add group order query page`。
2. 提交描述：说明查询页面筛选条件、视图读取逻辑和页面查询验证结果。

### Stage 13：P0 演示数据复盘与一键重置

覆盖需求：P0 演示数据要求 13.1 至 13.7。

Plan：

1. 复盘所有成功和失败案例是否会互相污染。
2. 通过重建 `schema.sql` 能恢复可演示初始状态。
3. 给每个评分点准备明确的示例输入。

Develop：

1. 调整 `schema.sql` 中的种子数据，使触发器、存储过程、事务、视图演示互不冲突。
2. 可新增 `docs/DEMO_CASES.md`，记录每个页面的建议输入和预期结果。
3. 若需要，补充操作日志写入，至少满足 P0-DB-009。

Verify：

1. 重建数据库后按 `docs/DEMO_CASES.md` 依次演示。
2. 确认触发器成功、触发器失败、存储过程成功、存储过程失败、事务成功、事务失败、视图查询都可稳定复现。
3. 确认失败案例不会破坏后续案例。

Commit：

1. 提交标题：`update: stabilize P0 demo data`。
2. 提交描述：说明演示数据调整、各评分点输入输出和完整演示复盘结果。

### Stage 14：README 与运行说明

覆盖需求：NF-001、NF-002、NF-003、最终交付物中的启动说明。

Plan：

1. README 面向助教演示，说明如何安装依赖、创建数据库、配置连接、启动项目、访问页面。
2. 不写真实密码，不写本机绝对路径。
3. 与实际文件和页面路径保持一致。

Develop：

1. 新增或更新 `README.md`。
2. 写明数据库脚本执行方式、连接配置项解释、Flask 启动方式和 P0 页面入口。
3. 写明常见问题，例如数据库连接失败、端口占用、未初始化数据库。

Verify：

1. 按 README 从干净数据库状态执行一遍。
2. 确认 README 中的命令、路径和页面地址与项目一致。
3. 检查 README 不含真实凭据、本机绝对路径或用户设备信息。

Commit：

1. 提交标题：`doc: add project runbook`。
2. 提交描述：说明 README 新增内容、运行流程验证和配置占位处理。

### Stage 15：报告素材与截图清单

覆盖需求：P0-RPT-001 至 P0-RPT-009、最终交付物中的截图和报告。

Plan：

1. 根据 `docs/REPORT_TEMPLATE.md` 建立可填写的报告素材清单。
2. 明确每个评分表格对应的源码位置、SQL 位置、页面路径和演示步骤。
3. 不在文档中写个人学号、姓名等敏感信息，保留占位符由提交前手动填写。

Develop：

1. 可新增 `docs/REPORT_FILLING_GUIDE.md` 或更新现有模板的辅助说明。
2. 列出页面截图：首页、加入拼单、完成拼单、取消拼单、查询页面。
3. 列出代码截图：连接代码、事务代码、触发器代码、存储过程代码、视图代码。
4. 列出数据库关系图截图生成建议。

Verify：

1. 按素材清单逐项确认每个评分点都有对应代码、SQL、页面或演示步骤。
2. 确认截图清单覆盖 3 到 4 张主要页面以及全部关键代码截图。
3. 检查文档中不含本机绝对路径、真实用户名、设备信息或真实密码。

Commit：

1. 提交标题：`doc: add report evidence guide`。
2. 提交描述：说明报告素材清单、截图点映射和敏感信息检查结果。

### Stage 16：P0 总体验收与修正

覆盖需求：P0 完成判定 17.1 至 17.15。

Plan：

1. 从干净数据库开始完整重放 P0。
2. 验收数据库、应用页面、业务操作、错误提示、事务回滚、报告素材。
3. 只做 P0 范围内的 bug 修复，不引入 P1/P2 功能。

Develop：

1. 修复验收中发现的 P0 bug。
2. 补齐缺失的错误处理、连接关闭、页面提示或文档说明。
3. 必要时补充最小验证脚本或 SQL 检查语句。

Verify：

1. 重建数据库并启动 Flask。
2. 访问 5 个 P0 页面。
3. 完成 7 类演示：触发器成功、触发器失败、存储过程成功、存储过程失败、事务成功、事务失败、视图查询。
4. 检查 `requirements.txt`、`README.md`、`schema.sql`、源码、模板和报告素材均存在。
5. 执行 `git status --short`，确认只存在本 stage 预期改动。

Commit：

1. 若有修复，提交标题：`fix: complete P0 acceptance fixes`。
2. 若只有文档验收补充，提交标题：`doc: finalize P0 acceptance checklist`。
3. 提交描述：说明最终验收发现、修复或补充内容、完整 P0 验证结果和剩余风险。

## 4. P0 覆盖矩阵

| 需求类别 | 主要 Stage |
| --- | --- |
| 数据库、表、外键、种子数据 | Stage 02 |
| Python MySQL 连接 | Stage 03 |
| 首页与基础统计 | Stage 01、Stage 04 |
| 触发器和加入拼单 | Stage 05、Stage 06 |
| 存储过程和完成拼单 | Stage 07、Stage 08 |
| 事务删除和取消拼单 | Stage 09、Stage 10 |
| 视图和详情查询 | Stage 11、Stage 12 |
| 演示数据稳定性 | Stage 13 |
| README 和运行说明 | Stage 14 |
| 报告素材和截图 | Stage 15 |
| 最终 P0 验收 | Stage 16 |

## 5. 后续执行方式

后续正式开发时，每次只启动一个 stage。每个 stage 的工作完成后，必须先完成 verify，再提交 commit，最后再进入下一 stage。

建议每个 stage 完成后记录：

1. 本 stage 实际改动文件。
2. 实际执行的验证命令或手工验证步骤。
3. 验证结果。
4. 提交哈希。
5. 遗留问题或下一 stage 依赖。
