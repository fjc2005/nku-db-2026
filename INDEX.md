# P0/P1/P2 任务实现索引

本文档用于作为后续 agent 的轻量上下文入口。正式开发时优先保留本索引，再按当前 stage 打开对应的需求片段和计划片段，避免一次性加载完整文档。

## 读取约定

1. 文档路径均为相对路径。
2. 行号格式为 `文档路径:L起始-L结束`。
3. 每个 stage 开始前先读取“公共上下文”和本 stage 对应条目。
4. 每个 stage 必须遵循 `plan -> develop -> verify -> commit` 闭环。
5. P0/P1/P2 均按对应 stage 计划推进；每次只推进当前 stage。

## 公共上下文

| 内容 | 索引 |
| --- | --- |
| 项目信息、背景、目标、角色、业务对象、系统边界 | `docs/REQUIREMENT.md:L1-L267` |
| P0 执行约定、范围摘要、Stage Gate 模板 | `docs/P0_BUILD.PLAN.md:L5-L55` |
| 数据库评分映射表 | `docs/REQUIREMENT.md:L1727-L1740` |
| P0 页面清单 | `docs/REQUIREMENT.md:L1741-L1752` |
| P0 数据库对象清单 | `docs/REQUIREMENT.md:L1753-L1769` |
| P1 需求范围 | `docs/REQUIREMENT.md:L1422-L1622` |
| P1 执行约定、范围摘要、Stage Gate 模板 | `docs/P1_BUILD.PLAN.md:L5-L64` |
| P1 覆盖矩阵、后续执行方式 | `docs/P1_BUILD.PLAN.md:L399-L424` |
| P2 需求范围 | `docs/REQUIREMENT.md:L1623-L1724` |
| P2 执行约定、范围摘要、Stage Gate 模板 | `docs/P2_BUILD.PLAN.md:L5-L69` |
| P2 覆盖矩阵、后续执行方式 | `docs/P2_BUILD.PLAN.md:L506-L532` |
| 最终交付物、推荐目录结构、P0 完成判定 | `docs/REQUIREMENT.md:L1984-L2042` |
| P0 覆盖矩阵、后续执行方式 | `docs/P0_BUILD.PLAN.md:L533-L559` |

## P0 Stage 对照目录

| Stage | 任务 | 需求文档索引 | 实现计划索引 | 本 stage 取用重点 |
| --- | --- | --- | --- | --- |
| Stage 00 | P0 搭建计划基线 | `docs/REQUIREMENT.md:L1-L267`, `docs/REQUIREMENT.md:L2023-L2042` | `docs/P0_BUILD.PLAN.md:L58-L83` | 建立计划基线，不写代码。 |
| Stage 01 | 项目骨架与依赖基线 | `docs/REQUIREMENT.md:L1905-L1944`, `docs/REQUIREMENT.md:L2001-L2022` | `docs/P0_BUILD.PLAN.md:L84-L110` | 只交付 Flask 骨架、依赖、首页占位。 |
| Stage 02 | 数据库基础表与演示种子数据 | `docs/REQUIREMENT.md:L270-L513`, `docs/REQUIREMENT.md:L1753-L1769`, `docs/REQUIREMENT.md:L1770-L1904` | `docs/P0_BUILD.PLAN.md:L111-L138` | 创建数据库、7 张业务表、外键和基础演示数据。 |
| Stage 03 | 数据库连接封装 | `docs/REQUIREMENT.md:L514-L561`, `docs/REQUIREMENT.md:L1945-L1958`, `docs/REQUIREMENT.md:L1970-L1983` | `docs/P0_BUILD.PLAN.md:L139-L165` | 统一 `get_connection()`，集中配置连接参数。 |
| Stage 04 | 首页真实统计接入 | `docs/REQUIREMENT.md:L562-L576`, `docs/REQUIREMENT.md:L1596-L1622` | `docs/P0_BUILD.PLAN.md:L166-L192` | 首页接入真实统计和 P0 操作入口。 |
| Stage 05 | 订单插入触发器 | `docs/REQUIREMENT.md:L635-L823`, `docs/REQUIREMENT.md:L499-L513`, `docs/REQUIREMENT.md:L1770-L1815` | `docs/P0_BUILD.PLAN.md:L193-L220` | 在 `schema.sql` 中实现触发器和成功/失败 SQL 演示数据。 |
| Stage 06 | 加入拼单页面与后端 | `docs/REQUIREMENT.md:L577-L593`, `docs/REQUIREMENT.md:L796-L823`, `docs/REQUIREMENT.md:L1970-L1983` | `docs/P0_BUILD.PLAN.md:L221-L249` | 页面路径 `/order/add`，参数化插入 `order_items`。 |
| Stage 07 | 完成拼单存储过程 | `docs/REQUIREMENT.md:L824-L961`, `docs/REQUIREMENT.md:L499-L513`, `docs/REQUIREMENT.md:L1816-L1847` | `docs/P0_BUILD.PLAN.md:L250-L278` | 在 `schema.sql` 中创建 `sp_finish_group_order`。 |
| Stage 08 | 完成拼单页面与 Python 调用 | `docs/REQUIREMENT.md:L594-L606`, `docs/REQUIREMENT.md:L923-L961`, `docs/REQUIREMENT.md:L1945-L1969` | `docs/P0_BUILD.PLAN.md:L279-L306` | 页面路径 `/group/finish`，通过 Python 调用存储过程。 |
| Stage 09 | 取消拼单事务服务 | `docs/REQUIREMENT.md:L962-L1116`, `docs/REQUIREMENT.md:L1959-L1983` | `docs/P0_BUILD.PLAN.md:L307-L335` | Python 显式事务、回滚、恢复库存和优惠券、JOIN 删除。 |
| Stage 10 | 取消拼单页面 | `docs/REQUIREMENT.md:L607-L619`, `docs/REQUIREMENT.md:L1087-L1116` | `docs/P0_BUILD.PLAN.md:L336-L363` | 页面路径 `/group/cancel`，展示取消成功和失败结果。 |
| Stage 11 | 拼单详情视图 | `docs/REQUIREMENT.md:L1117-L1258`, `docs/REQUIREMENT.md:L499-L513`, `docs/REQUIREMENT.md:L1886-L1904` | `docs/P0_BUILD.PLAN.md:L364-L391` | 在 `schema.sql` 中创建 `v_group_order_detail`。 |
| Stage 12 | 拼单详情查询页面 | `docs/REQUIREMENT.md:L620-L634`, `docs/REQUIREMENT.md:L1211-L1258`, `docs/REQUIREMENT.md:L1970-L1983` | `docs/P0_BUILD.PLAN.md:L392-L420` | 页面路径 `/group/query`，所有查询来自视图。 |
| Stage 13 | P0 演示数据复盘与一键重置 | `docs/REQUIREMENT.md:L1770-L1904`, `docs/REQUIREMENT.md:L1753-L1769` | `docs/P0_BUILD.PLAN.md:L421-L447` | 稳定所有成功/失败演示数据，避免案例互相污染。 |
| Stage 14 | README 与运行说明 | `docs/REQUIREMENT.md:L1905-L1944`, `docs/REQUIREMENT.md:L1984-L2022` | `docs/P0_BUILD.PLAN.md:L448-L474` | 补齐依赖安装、建库、配置、启动和页面访问说明。 |
| Stage 15 | 报告素材与截图清单 | `docs/REQUIREMENT.md:L1259-L1421`, `docs/REPORT_TEMPLATE.md:L1-L225` | `docs/P0_BUILD.PLAN.md:L475-L502` | 建立报告填写、页面截图、代码截图和关系图素材清单。 |
| Stage 16 | P0 总体验收与修正 | `docs/REQUIREMENT.md:L2023-L2042`, `docs/REQUIREMENT.md:L1727-L1904`, `docs/REQUIREMENT.md:L1984-L2000` | `docs/P0_BUILD.PLAN.md:L503-L532` | 从干净数据库完整重放 P0，修正验收发现的问题。 |

## P1 Stage 对照目录

| Stage | 任务 | 需求文档索引 | 实现计划索引 | 本 stage 取用重点 |
| --- | --- | --- | --- | --- |
| Stage 00 | P1 搭建计划基线 | `docs/REQUIREMENT.md:L1422-L1622` | `docs/P1_BUILD.PLAN.md:L67-L91` | 建立 P1 计划基线，不写代码。 |
| Stage 01 | P0 基线回归与 P1 验收清单 | `docs/REQUIREMENT.md:L1422-L1622`, `docs/REQUIREMENT.md:L2023-L2042` | `docs/P1_BUILD.PLAN.md:L93-L120` | 先确认 P0 可运行，再建立 P1 验收清单。 |
| Stage 02 | 学生与店铺列表页面 | `docs/REQUIREMENT.md:L1426-L1447` | `docs/P1_BUILD.PLAN.md:L122-L150` | 页面路径 `/data/students` 和 `/data/shops`，只读展示基础数据。 |
| Stage 03 | 饮品与优惠券列表页面 | `docs/REQUIREMENT.md:L1450-L1470` | `docs/P1_BUILD.PLAN.md:L152-L181` | 页面路径 `/data/drinks` 和 `/data/coupons`，展示库存和优惠券状态变化。 |
| Stage 04 | 加入拼单动态下拉表单 | `docs/REQUIREMENT.md:L1473-L1517` | `docs/P1_BUILD.PLAN.md:L183-L213` | `/order/add` 使用学生、拼单、饮品、优惠券数据库下拉选项。 |
| Stage 05 | 表单校验与友好错误提示 | `docs/REQUIREMENT.md:L1566-L1590` | `docs/P1_BUILD.PLAN.md:L215-L245` | 处理空值、数量校验和数据库错误页面提示，不暴露堆栈。 |
| Stage 06 | 成功业务操作日志写入 | `docs/REQUIREMENT.md:L1520-L1552` | `docs/P1_BUILD.PLAN.md:L247-L276` | 加入、完成、取消成功后写入 `operation_logs`。 |
| Stage 07 | 操作日志查看页面 | `docs/REQUIREMENT.md:L1555-L1562` | `docs/P1_BUILD.PLAN.md:L278-L306` | 页面路径 `/logs`，按时间倒序展示操作日志。 |
| Stage 08 | 首页演示入口与统计卡片增强 | `docs/REQUIREMENT.md:L1594-L1619` | `docs/P1_BUILD.PLAN.md:L308-L336` | 首页展示四类评分操作入口和五个核心统计卡片。 |
| Stage 09 | P1 演示说明与运行文档补充 | `docs/REQUIREMENT.md:L1450-L1470`, `docs/REQUIREMENT.md:L1520-L1562`, `docs/REQUIREMENT.md:L1594-L1619` | `docs/P1_BUILD.PLAN.md:L338-L365` | 补充 P1 演示路线、截图点和页面入口说明。 |
| Stage 10 | P1 总体验收与回归修正 | `docs/REQUIREMENT.md:L1422-L1622` | `docs/P1_BUILD.PLAN.md:L367-L397` | 从干净数据库完整重放 P0 和 P1，修正验收发现的问题。 |

## P2 Stage 对照目录

| Stage | 任务 | 需求文档索引 | 实现计划索引 | 本 stage 取用重点 |
| --- | --- | --- | --- | --- |
| Stage 00 | P2 搭建计划基线 | `docs/REQUIREMENT.md:L1623-L1724` | `docs/P2_BUILD.PLAN.md:L73-L97` | 建立 P2 计划基线，不写代码。 |
| Stage 01 | P0/P1 基线回归与 P2 验收清单 | `docs/REQUIREMENT.md:L1623-L1724` | `docs/P2_BUILD.PLAN.md:L99-L127` | 先确认 P0/P1 可运行，再建立 P2 验收清单。 |
| Stage 02 | 登录账号数据模型与演示账号 | `docs/REQUIREMENT.md:L1627-L1648` | `docs/P2_BUILD.PLAN.md:L129-L157` | 在 `schema.sql` 中增加演示账号表、角色约束和密码哈希种子数据。 |
| Stage 03 | 登录、退出与会话基础 | `docs/REQUIREMENT.md:L1629-L1637` | `docs/P2_BUILD.PLAN.md:L159-L189` | 页面路径 `/login`、`/logout`，实现 Flask session 登录流。 |
| Stage 04 | 角色导航与页面访问控制 | `docs/REQUIREMENT.md:L1641-L1648` | `docs/P2_BUILD.PLAN.md:L191-L220` | 按学生/管理员角色展示入口并限制受保护页面。 |
| Stage 05 | 学生参与拼单与个人订单范围 | `docs/REQUIREMENT.md:L1641-L1648` | `docs/P2_BUILD.PLAN.md:L222-L251` | 学生下单绑定当前账号，学生查询只看自己的订单。 |
| Stage 06 | 创建拼单页面 | `docs/REQUIREMENT.md:L1654-L1663` | `docs/P2_BUILD.PLAN.md:L253-L283` | 页面路径 `/group/create`，选择店铺、标题、截止时间并创建 `OPEN` 拼单。 |
| Stage 07 | 过期拼单自动关闭 | `docs/REQUIREMENT.md:L1667-L1675` | `docs/P2_BUILD.PLAN.md:L285-L314` | 超过 `deadline_at` 的 `OPEN` 拼单自动关闭，且不能继续加入。 |
| Stage 08 | 拼单备注字段与展示 | `docs/REQUIREMENT.md:L1679-L1686` | `docs/P2_BUILD.PLAN.md:L316-L345` | `order_items` 增加备注字段，加入拼单可填写，详情查询可显示。 |
| Stage 09 | 饮品销量排行 | `docs/REQUIREMENT.md:L1692-L1700` | `docs/P2_BUILD.PLAN.md:L347-L376` | 页面路径 `/stats/drinks`，按饮品统计销量并倒序展示。 |
| Stage 10 | 学生消费排行 | `docs/REQUIREMENT.md:L1704-L1712` | `docs/P2_BUILD.PLAN.md:L378-L407` | 页面路径 `/stats/students`，按学生统计实付金额并倒序展示。 |
| Stage 11 | 拼单详情 CSV 导出 | `docs/REQUIREMENT.md:L1716-L1723` | `docs/P2_BUILD.PLAN.md:L409-L439` | 页面路径 `/group/query/export`，导出与详情查询筛选一致的 CSV。 |
| Stage 12 | P2 演示说明与运行文档补充 | `docs/REQUIREMENT.md:L1623-L1724` | `docs/P2_BUILD.PLAN.md:L441-L468` | 补充 P2 演示路线、截图点、页面入口和登录说明。 |
| Stage 13 | P2 总体验收与回归修正 | `docs/REQUIREMENT.md:L1623-L1724` | `docs/P2_BUILD.PLAN.md:L470-L504` | 从干净数据库完整重放 P0、P1 和 P2，修正验收发现的问题。 |

## 需求速查

| 需求类别 | 索引 |
| --- | --- |
| P0 数据库需求 | `docs/REQUIREMENT.md:L270-L513` |
| P0 Python 连接需求 | `docs/REQUIREMENT.md:L514-L561` |
| P0 页面需求 | `docs/REQUIREMENT.md:L562-L634` |
| P0 触发器添加需求 | `docs/REQUIREMENT.md:L635-L823` |
| P0 存储过程更新需求 | `docs/REQUIREMENT.md:L824-L961` |
| P0 事务删除需求 | `docs/REQUIREMENT.md:L962-L1116` |
| P0 视图查询需求 | `docs/REQUIREMENT.md:L1117-L1258` |
| P0 报告与截图需求 | `docs/REQUIREMENT.md:L1259-L1421` |
| P0 演示数据要求 | `docs/REQUIREMENT.md:L1770-L1904` |
| P1 基础数据管理需求 | `docs/REQUIREMENT.md:L1426-L1470` |
| P1 表单体验需求 | `docs/REQUIREMENT.md:L1473-L1517` |
| P1 操作日志需求 | `docs/REQUIREMENT.md:L1520-L1562` |
| P1 错误提示需求 | `docs/REQUIREMENT.md:L1566-L1590` |
| P1 演示辅助需求 | `docs/REQUIREMENT.md:L1594-L1619` |
| P2 登录权限需求 | `docs/REQUIREMENT.md:L1627-L1648` |
| P2 拼单体验需求 | `docs/REQUIREMENT.md:L1652-L1686` |
| P2 数据展示需求 | `docs/REQUIREMENT.md:L1690-L1723` |
| 非功能需求 | `docs/REQUIREMENT.md:L1905-L1983` |

## Agent 执行提示

1. 每次只推进一个 stage。
2. 当前 stage 的代码开发前，先用本索引定位并读取相关需求和计划。
3. 若 stage 涉及报告评分点，同时读取 `docs/REPORT_TEMPLATE.md` 对应章节。
4. 每个 stage 完成后记录实际改动文件、验证步骤、提交哈希和遗留问题。
5. 文档、配置示例和提交描述不得写入真实凭据、个人身份信息或本机环境细节。
