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
