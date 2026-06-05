# P0 任务实现索引

本文档用于作为后续 agent 的轻量上下文入口。正式开发时优先保留本索引，再按当前 stage 打开对应的需求片段和计划片段，避免一次性加载完整文档。

## 读取约定

1. 文档路径均为相对路径。
2. 行号格式为 `文档路径:L起始-L结束`。
3. 每个 stage 开始前先读取“公共上下文”和本 stage 对应条目。
4. 每个 stage 必须遵循 `plan -> develop -> verify -> commit` 闭环。
5. P0 阶段只实现最低评分必需功能；P1/P2 需求仅作后续扩展参考。

## 公共上下文

| 内容 | 索引 |
| --- | --- |
| 项目信息、背景、目标、角色、业务对象、系统边界 | `docs/REQUIREMENT.md:L1-L267` |
| P0 执行约定、范围摘要、Stage Gate 模板 | `docs/P0_BUILD.PLAN.md:L5-L55` |
| 数据库评分映射表 | `docs/REQUIREMENT.md:L1727-L1740` |
| P0 页面清单 | `docs/REQUIREMENT.md:L1741-L1752` |
| P0 数据库对象清单 | `docs/REQUIREMENT.md:L1753-L1769` |
| 最终交付物、推荐目录结构、P0 完成判定 | `docs/REQUIREMENT.md:L1984-L2042` |
| P0 覆盖矩阵、后续执行方式 | `docs/P0_BUILD.PLAN.md:L533-L559` |

## Stage 对照目录

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
| 非功能需求 | `docs/REQUIREMENT.md:L1905-L1983` |

## Agent 执行提示

1. 每次只推进一个 stage。
2. 当前 stage 的代码开发前，先用本索引定位并读取相关需求和计划。
3. 若 stage 涉及报告评分点，同时读取 `docs/REPORT_TEMPLATE.md` 对应章节。
4. 每个 stage 完成后记录实际改动文件、验证步骤、提交哈希和遗留问题。
5. 文档、配置示例和提交描述不得写入真实凭据、个人身份信息或本机环境细节。
