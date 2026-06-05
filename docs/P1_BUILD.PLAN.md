# P1 分 Stage 搭建计划

本文档用于指导“校园奶茶拼单系统”P1 范围的逐 stage 实施。P1 只在 P0 已可运行、可演示的基础上提升系统完整度和演示观感；每个 stage 都必须形成 `plan -> develop -> verify -> commit` 闭环。

## 0. 执行约定

1. 开始 P1 前必须先确认 P0 核心流程仍可运行：加入拼单、完成拼单、取消拼单、拼单详情查询。
2. 每个 stage 开始前，先确认本 stage 的目标、覆盖的 P1 条目、涉及文件、依赖的 P0 能力和验收方式。
3. 每个 stage 只实现当前范围，不提前实现 P2 登录、二维码、移动端适配、导出或图表统计。
4. Commit title 使用 `<action>: <message>` 格式；`action` 优先使用 `update`、`fix`、`delete`、`doc`。
5. 每个 commit 除标题外必须包含详细描述正文，说明本次变更内容、验证结果和影响范围。
6. 文档、配置示例和 README 不写入本机绝对路径、真实用户名、设备信息或真实数据库密码。
7. 运行 Python 或 Flask 前先激活项目约定的 conda 环境；依赖变更必须同步更新 `requirements.txt`。
8. Python SQL 操作必须使用参数化查询；事务失败必须 rollback；数据库连接和 cursor 必须关闭。
9. P1 不新增数据库表；操作日志复用 P0 的 `operation_logs` 表。
10. P1 日志需求只要求成功操作写入日志，失败操作是否记录不作为本阶段强制范围。
11. P1 基础数据管理按“查看列表”实现，不包含新增、编辑、删除基础数据。

## 1. P1 范围摘要

P1 交付目标是让 P0 系统更适合现场演示和日常查看：

1. 提供基础数据查看页面：学生、店铺、饮品、优惠券。
2. 将加入拼单页面的编号输入升级为数据库下拉选择。
3. 成功加入拼单、完成拼单、取消拼单后写入操作日志。
4. 提供操作日志查看页面，按时间倒序展示日志。
5. 改善数据库错误和表单空值错误的页面提示。
6. 首页展示四类评分操作入口和核心统计卡片。
7. 更新演示说明和验收清单，确保 P1 不破坏 P0 评分操作。

建议 P1 新增页面路径：

| 页面名称 | 路径 | 覆盖需求 |
| --- | --- | --- |
| 学生列表 | `/data/students` | P1-DATA-001 |
| 店铺列表 | `/data/shops` | P1-DATA-002 |
| 饮品列表 | `/data/drinks` | P1-DATA-003 |
| 优惠券列表 | `/data/coupons` | P1-DATA-004 |
| 操作日志 | `/logs` | P1-LOG-004 |

## 2. Stage Gate 模板

每个 stage 必须按以下格式执行：

| 步骤 | 要求 |
| --- | --- |
| Plan | 明确本 stage 目标、覆盖需求、改动文件、依赖关系、风险和验收命令。 |
| Develop | 只实现本 stage 范围内的文件改动，不提前实现后续 stage。 |
| Verify | 执行本 stage 的最小可验证检查，并记录结果；涉及页面时至少做页面打开和数据正确性检查。 |
| Commit | 验证通过后提交；提交标题使用 `<action>: <message>`；提交正文写清变更内容、验证结果和影响范围。 |

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

### Stage 00：P1 搭建计划基线

覆盖需求：P1 范围拆分、P1 执行约定。

Plan：

1. 阅读 `INDEX.md`、`docs/REQUIREMENT.md` 和 `docs/P0_BUILD.PLAN.md`，提取 P1 必须项和 P0 文档写法。
2. 设计 P1 stage，使每个 stage 都有明确可验证成果和提交边界。
3. 确认计划文档不包含本机绝对路径、真实凭据或用户设备信息。

Develop：

1. 新增 `docs/P1_BUILD.PLAN.md`。
2. 写入全局执行约定、P1 摘要、stage gate 和逐 stage 实施计划。

Verify：

1. 检查文档存在且 Markdown 可读。
2. 检查文档仅使用相对路径、页面路径和占位符。
3. 检查每个 stage 都包含 Plan、Develop、Verify、Commit。

Commit：

1. 提交标题：`doc: add P1 staged build plan`。
2. 提交描述：说明新增 P1 分 stage 搭建计划、已验证闭环结构和敏感信息检查结果。

### Stage 01：P0 基线回归与 P1 验收清单

覆盖需求：P1 全部需求的前置依赖、P1 不破坏 P0 核心评分操作。

Plan：

1. 从干净数据库和当前 Flask 应用状态确认 P0 核心流程可运行。
2. 建立 P1 验收清单，后续每个 stage 完成后更新实际验证结果。
3. 只记录和修复阻塞 P1 的 P0 基线问题，不扩展 P1 功能。

Develop：

1. 可新增 `docs/P1_ACCEPTANCE_CHECKLIST.md`。
2. 清单包含 P1 需求编号、对应页面或代码位置、验证方法、当前状态和备注。
3. 若发现 P0 阻塞问题，只做最小修复并记录影响范围。

Verify：

1. 激活 conda 环境后安装依赖：`pip install -r requirements.txt`。
2. 重建数据库并启动 Flask：`python app.py`。
3. 访问 `/`、`/order/add`、`/group/finish`、`/group/cancel`、`/group/query`。
4. 至少执行一次 P0 触发器成功、存储过程成功、事务失败回滚和视图查询验证。
5. 检查新增验收清单不含真实凭据、本机绝对路径或个人信息。

Commit：

1. 提交标题：`doc: add P1 acceptance checklist`。
2. 提交描述：说明 P0 基线回归结果、P1 验收清单内容和未解决风险。

### Stage 02：学生与店铺列表页面

覆盖需求：P1-DATA-001、P1-DATA-002。

Plan：

1. 先实现最简单的只读基础数据页面。
2. 页面路径固定为 `/data/students` 和 `/data/shops`。
3. 列表数据必须来自 MySQL，不使用静态样例数据。

Develop：

1. 更新 `app.py`，新增学生列表和店铺列表 GET 路由。
2. 新增 `templates/data_students.html` 和 `templates/data_shops.html`。
3. 更新 `templates/base.html` 或首页导航，提供基础数据入口。
4. 查询使用参数化或无用户输入的固定 SQL，并确保 cursor 和 connection 关闭。

Verify：

1. 启动 Flask，访问 `/data/students`。
2. 确认页面显示学生编号、姓名、手机号、状态，记录数与数据库一致。
3. 访问 `/data/shops`。
4. 确认页面显示店铺编号、店铺名称、校区位置、状态，记录数与数据库一致。
5. 暂停数据库或模拟数据库错误时，页面不暴露堆栈。

Commit：

1. 提交标题：`update: add student and shop list pages`。
2. 提交描述：说明新增学生和店铺列表页面、导航入口和页面读取验证结果。

### Stage 03：饮品与优惠券列表页面

覆盖需求：P1-DATA-003、P1-DATA-004。

Plan：

1. 实现可展示关联信息的只读列表页面。
2. 饮品列表显示店铺名称，优惠券列表显示学生姓名。
3. 页面应能支撑下单前后库存和优惠券状态变化演示。

Develop：

1. 更新 `app.py`，新增 `/data/drinks` 和 `/data/coupons` GET 路由。
2. 新增 `templates/data_drinks.html` 和 `templates/data_coupons.html`。
3. 饮品查询关联 `drinks` 和 `shops`。
4. 优惠券查询关联 `coupons` 和 `students`。
5. 更新导航或首页基础数据入口。

Verify：

1. 访问 `/data/drinks`，确认显示饮品编号、店铺名称、饮品名称、价格、库存、状态。
2. 访问 `/data/coupons`，确认显示优惠券编号、学生姓名、优惠金额、最低使用金额、有效期、状态。
3. 执行一次合法加入拼单后刷新饮品页，确认库存变化可见。
4. 使用优惠券加入拼单后刷新优惠券页，确认优惠券状态变化可见。
5. 检查关联查询不直接拼接用户输入。

Commit：

1. 提交标题：`update: add drink and coupon list pages`。
2. 提交描述：说明新增饮品和优惠券列表、关联展示字段和状态变化验证结果。

### Stage 04：加入拼单动态下拉表单

覆盖需求：P1-FORM-001、P1-FORM-002、P1-FORM-003、P1-FORM-004。

Plan：

1. 将 `/order/add` 的编号输入升级为数据库下拉选择。
2. 学生、拼单、饮品、优惠券选项均来自 MySQL。
3. 优惠券下拉支持“不使用优惠券”；本 stage 不强制实现按学生联动过滤。

Develop：

1. 更新 `/order/add` GET 路由，查询学生、拼单、饮品、优惠券选项。
2. 更新 `templates/add_order.html`，将学生编号、拼单编号、饮品编号、优惠券编号改为下拉框。
3. 拼单选项优先显示 `OPEN` 状态拼单。
4. 优惠券选项优先显示 `UNUSED` 状态优惠券，并保留空值表示不使用优惠券。
5. POST 逻辑继续沿用参数化插入，金额和库存仍由触发器处理。

Verify：

1. 打开 `/order/add`，确认学生下拉显示学生姓名和编号。
2. 确认拼单下拉显示拼单标题和编号，`OPEN` 状态优先。
3. 确认饮品下拉显示饮品名称、价格和库存。
4. 确认优惠券下拉显示优惠券名称和优惠金额，并支持不使用优惠券。
5. 提交一组合法数据，确认仍可成功加入拼单。
6. 提交不使用优惠券的数据，确认订单可创建且优惠金额为 0。

Commit：

1. 提交标题：`update: add order form dropdowns`。
2. 提交描述：说明加入拼单表单下拉数据来源、选项排序规则和成功提交验证结果。

### Stage 05：表单校验与友好错误提示

覆盖需求：P1-ERR-001、P1-ERR-002。

Plan：

1. 统一处理 P0 操作页面的常见错误提示。
2. 表单空值和数量非正整数错误先在 Flask 层拦截。
3. 数据库触发器、存储过程和事务错误只显示用户可读原因，不展示完整堆栈。

Develop：

1. 可在 `app.py` 中新增表单校验和错误消息辅助函数。
2. 更新 `/order/add` POST，校验拼单、学生、饮品、数量必填，数量必须为正整数。
3. 更新 `/group/finish` 和 `/group/cancel` POST，校验拼单编号必填且格式有效。
4. 捕获 MySQL 错误并提取简短错误信息用于页面展示。
5. 更新相关模板的成功和失败提示样式。

Verify：

1. 在 `/order/add` 提交空表单，确认页面提示必填项。
2. 在 `/order/add` 提交数量为 0、负数或非数字，确认页面提示数量必须为正整数。
3. 提交 LOCKED 学生或库存不足案例，确认触发器错误以页面提示展示。
4. 在 `/group/finish` 重复完成同一拼单，确认存储过程错误以页面提示展示。
5. 在 `/group/cancel` 取消已完成拼单，确认事务失败提示且数据库数据不变。
6. 检查页面和日志输出不展示完整 Python 堆栈。

Commit：

1. 提交标题：`fix: improve form validation and error messages`。
2. 提交描述：说明表单校验规则、数据库错误提示处理和失败案例验证结果。

### Stage 06：成功业务操作日志写入

覆盖需求：P1-LOG-001、P1-LOG-002、P1-LOG-003。

Plan：

1. 复用 `operation_logs` 表记录成功业务操作。
2. 日志写入跟随对应业务事务提交，避免业务失败却留下成功日志。
3. 本 stage 只写入日志，不实现日志查看页面。

Develop：

1. 可在 `app.py` 中新增 `write_operation_log()` 辅助函数。
2. 加入拼单成功后写入 `ADD_ORDER_ITEM`，内容包含学生编号、拼单编号、饮品编号。
3. 完成拼单成功后写入 `FINISH_GROUP_ORDER`，内容包含拼单编号和总金额。
4. 取消拼单成功后写入 `CANCEL_GROUP_ORDER`，内容包含拼单编号。
5. 确保日志写入使用参数化 SQL，并与对应业务 commit 顺序一致。

Verify：

1. 重建数据库后执行一次成功加入拼单。
2. 查询 `operation_logs`，确认存在 `ADD_ORDER_ITEM` 且内容包含学生编号、拼单编号、饮品编号。
3. 执行一次成功完成拼单，确认存在 `FINISH_GROUP_ORDER` 且内容包含拼单编号和总金额。
4. 执行一次成功取消拼单，确认存在 `CANCEL_GROUP_ORDER` 且内容包含拼单编号。
5. 执行一个失败案例，确认不会写入对应成功日志。

Commit：

1. 提交标题：`update: record successful operation logs`。
2. 提交描述：说明三个成功操作的日志写入位置、日志内容和数据库验证结果。

### Stage 07：操作日志查看页面

覆盖需求：P1-LOG-004。

Plan：

1. 页面路径固定为 `/logs`。
2. 日志页面只读展示 `operation_logs`。
3. 默认按操作时间倒序显示，便于现场演示最近操作。

Develop：

1. 更新 `app.py`，新增 `/logs` GET 路由。
2. 新增 `templates/operation_logs.html`。
3. 页面显示操作类型、操作说明、操作时间。
4. 在首页或导航中新增操作日志入口。

Verify：

1. 执行加入、完成、取消至少一种成功操作生成日志。
2. 访问 `/logs`，确认页面显示操作类型、操作说明、操作时间。
3. 确认日志按时间倒序显示。
4. 确认空日志状态下页面仍可正常显示。
5. 检查日志页面查询不包含用户输入拼接。

Commit：

1. 提交标题：`update: add operation log page`。
2. 提交描述：说明日志页面、排序规则、导航入口和页面验证结果。

### Stage 08：首页演示入口与统计卡片增强

覆盖需求：P1-DEMO-001、P1-DEMO-002。

Plan：

1. 首页作为现场演示入口，展示四类评分操作快捷入口。
2. 首页统计卡片从数据库读取真实数据。
3. 在不改变 P0 核心路径的前提下补充 P1 基础数据和日志入口。

Develop：

1. 更新 `/` 路由统计查询，返回学生数量、店铺数量、饮品数量、进行中拼单数量、已完成拼单数量。
2. 更新 `templates/index.html`，展示核心统计卡片。
3. 首页保留“加入拼单”“完成拼单”“取消拼单”“拼单详情查询”四类入口。
4. 可补充学生、店铺、饮品、优惠券、日志页面入口。
5. 数据库异常时首页显示友好提示，不暴露堆栈。

Verify：

1. 访问 `/`，确认四类评分操作入口均存在且可跳转。
2. 确认首页显示学生数量、店铺数量、饮品数量、进行中拼单数量、已完成拼单数量。
3. 修改数据库中拼单状态或重建数据后刷新首页，确认统计数值同步变化。
4. 点击 P1 基础数据和日志入口，确认链接可达。

Commit：

1. 提交标题：`update: enhance homepage demo dashboard`。
2. 提交描述：说明首页统计卡片、演示入口和链接跳转验证结果。

### Stage 09：P1 演示说明与运行文档补充

覆盖需求：P1-DATA-003、P1-DATA-004、P1-LOG-001 至 P1-LOG-004、P1-DEMO-001、P1-DEMO-002 的演示支撑。

Plan：

1. 补充 P1 演示路线，方便后续截图和现场讲解。
2. 文档只记录页面路径、建议输入、预期变化和验证 SQL，不记录真实凭据或个人信息。
3. 与已有 P0 演示数据说明保持一致。

Develop：

1. 更新 `docs/DEMO_CASES.md`，补充 P1 演示顺序。
2. 可更新 `README.md`，补充 P1 页面入口说明。
3. 可更新 `docs/P1_ACCEPTANCE_CHECKLIST.md`，标记已完成 stage 的验证状态。
4. 记录库存变化、优惠券状态变化、操作日志新增、首页统计变化的演示步骤。

Verify：

1. 按 P1 演示说明从干净数据库状态执行一遍。
2. 确认每个 P1 页面都可截图且数据稳定。
3. 确认 README 或演示文档中的页面路径与实际路由一致。
4. 检查文档不含真实凭据、本机绝对路径、真实用户名或设备信息。

Commit：

1. 提交标题：`doc: add P1 demo guide`。
2. 提交描述：说明 P1 演示路线、页面入口、验证结果和敏感信息检查结果。

### Stage 10：P1 总体验收与回归修正

覆盖需求：P1-DATA-001 至 P1-DATA-004、P1-FORM-001 至 P1-FORM-004、P1-LOG-001 至 P1-LOG-004、P1-ERR-001 至 P1-ERR-002、P1-DEMO-001 至 P1-DEMO-002。

Plan：

1. 从干净数据库开始完整重放 P0 和 P1。
2. 验收 P1 页面、下拉表单、错误提示、日志写入、首页统计和演示文档。
3. 只修复 P1 验收发现的问题，不引入 P2 功能。

Develop：

1. 修复验收中发现的 P1 bug。
2. 补齐缺失的连接关闭、页面提示、导航入口或文档说明。
3. 必要时补充最小验证 SQL 或检查清单。

Verify：

1. 重建数据库并启动 Flask。
2. 访问 P0 页面：`/`、`/order/add`、`/group/finish`、`/group/cancel`、`/group/query`。
3. 访问 P1 页面：`/data/students`、`/data/shops`、`/data/drinks`、`/data/coupons`、`/logs`。
4. 验证加入拼单下拉框、空值校验、数量校验和数据库错误提示。
5. 完成一次加入、完成、取消成功操作，确认日志写入并在 `/logs` 倒序显示。
6. 验证首页五个统计卡片和四类评分操作入口。
7. 执行 `git status --short`，确认只存在本 stage 预期改动。

Commit：

1. 若有代码修复，提交标题：`fix: complete P1 acceptance fixes`。
2. 若只有文档验收补充，提交标题：`doc: finalize P1 acceptance checklist`。
3. 提交描述：说明最终验收发现、修复或补充内容、完整 P1 验证结果和剩余风险。

## 4. P1 覆盖矩阵

| 需求类别 | 主要 Stage |
| --- | --- |
| P1 计划和验收清单 | Stage 00、Stage 01 |
| 学生和店铺列表 | Stage 02 |
| 饮品和优惠券列表 | Stage 03 |
| 加入拼单动态下拉框 | Stage 04 |
| 表单校验和友好错误提示 | Stage 05 |
| 成功业务操作日志写入 | Stage 06 |
| 操作日志查看页面 | Stage 07 |
| 首页演示入口和统计卡片 | Stage 08 |
| P1 演示说明和运行文档 | Stage 09 |
| P1 总体验收和 P0 回归 | Stage 10 |

## 5. 后续执行方式

后续正式开发时，每次只启动一个 stage。每个 stage 的工作完成后，必须先完成 verify，再提交 commit，最后再进入下一 stage。

建议每个 stage 完成后记录：

1. 本 stage 实际改动文件。
2. 实际执行的验证命令或手工验证步骤。
3. 验证结果。
4. 提交哈希。
5. 遗留问题或下一 stage 依赖。
