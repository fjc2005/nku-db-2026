# P0 Acceptance Checklist

This checklist records the final P0 acceptance evidence available in the current
workspace. Live database operation verification requires a running MySQL service
and a fresh import of `schema.sql`.

## Local Verification Performed

| Check | Result |
| --- | --- |
| Python compile check for `app.py` and `db.py` | Passed |
| Flask test client `GET /` | Passed, HTTP 200 |
| Flask test client `GET /order/add` | Passed, HTTP 200 |
| Flask test client `GET /group/finish` | Passed, HTTP 200 |
| Flask test client `GET /group/cancel` | Passed, HTTP 200 |
| Flask test client `GET /group/query` | Passed, HTTP 200 |
| Required deliverables exist | Passed |
| Documentation sensitive-path scan | Passed |
| MySQL client availability | Not available in this environment |
| MySQL service connection | Not available on `127.0.0.1:3306` in this environment |

## Requirement Evidence

| P0 condition | Evidence |
| --- | --- |
| MySQL database script exists | `schema.sql` creates `milk_tea_group_db` |
| Python connects through one helper | `db.py` contains `DB_CONFIG` and `get_connection()` |
| Five P0 pages exist | `/`, `/order/add`, `/group/finish`, `/group/cancel`, `/group/query` |
| Seven business tables exist | `schema.sql` creates `students`, `shops`, `drinks`, `group_orders`, `coupons`, `order_items`, `operation_logs` |
| Foreign keys exist | `schema.sql` contains eight named `fk_` constraints |
| Trigger-controlled add exists | `schema.sql` creates `trg_before_order_item_insert`; `/order/add` inserts `order_items` |
| Trigger success/failure cases exist | `docs/DEMO_CASES.md` sections 1 and 2 |
| Stored procedure update exists | `schema.sql` creates `sp_finish_group_order`; `app.py` calls it with `callproc` |
| Stored procedure success/failure cases exist | `docs/DEMO_CASES.md` sections 3 and 4 |
| Explicit transaction cancel exists | `app.py` contains `start_transaction()`, `commit()`, `rollback()`, and JOIN delete SQL |
| Transaction success/failure cases exist | `docs/DEMO_CASES.md` sections 5 and 6 |
| View-based query exists | `schema.sql` creates `v_group_order_detail`; `/group/query` reads from it |
| Report evidence exists | `docs/REPORT_FILLING_GUIDE.md` maps report sections to code, SQL, screenshots, and demos |
| Run instructions exist | `README.md` documents setup, database import, configuration, startup, and page paths |

## Live MySQL Verification To Run

After starting MySQL and importing `schema.sql`, run the walkthrough in
`docs/DEMO_CASES.md`:

1. Trigger success and failure from `/order/add`.
2. Stored procedure success and repeat failure from `/group/finish`.
3. Transaction failure and success from `/group/cancel`.
4. View filters from `/group/query`.

Recommended SQL checks after import:

```sql
SHOW TABLES;
SHOW TRIGGERS LIKE 'order_items';
SHOW PROCEDURE STATUS WHERE Db = 'milk_tea_group_db';
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SELECT COUNT(*) FROM v_group_order_detail;
```
