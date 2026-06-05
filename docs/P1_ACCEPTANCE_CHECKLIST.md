# P1 Acceptance Checklist

This checklist tracks P1 requirements, implementation targets, verification steps, and final acceptance status. It assumes a clean database created from `schema.sql` before full regression.

## Scope

| Requirement | Target | Verification | Status | Notes |
| --- | --- | --- | --- | --- |
| P1-DATA-001 | `/data/students` | Page shows student number, name, phone, and status for all students. | Implemented; DB pending | Stage 02 |
| P1-DATA-002 | `/data/shops` | Page shows shop ID, shop name, campus location, and status for all shops. | Implemented; DB pending | Stage 02 |
| P1-DATA-003 | `/data/drinks` | Page shows drink ID, shop name, drink name, price, stock, and status; stock change is visible after adding an order. | Implemented; DB pending | Stage 03 |
| P1-DATA-004 | `/data/coupons` | Page shows coupon ID, student name, amount, minimum order amount, validity date, and status; coupon status change is visible after adding an order. | Implemented; DB pending | Stage 03 |
| P1-FORM-001 | `/order/add` | Student selection is a database-backed dropdown showing student name and number. | Implemented; DB pending | Stage 04 |
| P1-FORM-002 | `/order/add` | Group order selection is a database-backed dropdown showing title and ID, with `OPEN` orders first. | Implemented; DB pending | Stage 04 |
| P1-FORM-003 | `/order/add` | Drink selection is a database-backed dropdown showing drink name, price, and stock. | Implemented; DB pending | Stage 04 |
| P1-FORM-004 | `/order/add` | Coupon selection is a database-backed dropdown showing coupon name and amount, supports no coupon, and lists `UNUSED` coupons first. | Implemented; DB pending | Stage 04 |
| P1-ERR-001 | P0 operation pages | Database trigger, procedure, and transaction errors are displayed as user-readable page messages without stack traces. | Smoke passed; DB pending | Stage 05 |
| P1-ERR-002 | `/order/add` | Required fields are checked and quantity must be a positive integer. | Smoke passed; DB pending | Stage 05 |
| P1-LOG-001 | `operation_logs` | Successful add order writes `ADD_ORDER_ITEM` with student ID, group order ID, and drink ID. | Implemented; DB pending | Stage 06 |
| P1-LOG-002 | `operation_logs` | Successful finish group writes `FINISH_GROUP_ORDER` with group order ID and total amount. | Implemented; DB pending | Stage 06 |
| P1-LOG-003 | `operation_logs` | Successful cancel group writes `CANCEL_GROUP_ORDER` with group order ID. | Implemented; DB pending | Stage 06 |
| P1-LOG-004 | `/logs` | Page shows operation type, detail, and time in reverse chronological order. | Implemented; DB pending | Stage 07 |
| P1-DEMO-001 | `/` | Homepage shows quick entries for add order, finish group, cancel group, and group detail query. | Smoke passed; DB pending | Stage 08 |
| P1-DEMO-002 | `/` | Homepage shows student count, shop count, drink count, open group count, and finished group count. | Smoke passed; DB pending | Stage 08 |

## Baseline Regression

| Check | Method | Result |
| --- | --- | --- |
| Dependencies installed | `pip install -r requirements.txt` after activating the conda environment | Passed |
| Python syntax | `python -m py_compile app.py db.py` after activating the conda environment | Passed |
| MySQL client availability | `command -v mysql` | Blocked: CLI client not available in this shell |
| Clean database replay | Execute `schema.sql` against MySQL | Pending |
| P0 page smoke | Visit `/`, `/order/add`, `/group/finish`, `/group/cancel`, `/group/query` | Pending |
| P0 trigger success/failure | Follow `docs/DEMO_CASES.md` add order cases | Pending |
| P0 stored procedure success/failure | Follow `docs/DEMO_CASES.md` finish group cases | Pending |
| P0 transaction success/failure | Follow `docs/DEMO_CASES.md` cancel group cases | Pending |
| P0 view query | Follow `docs/DEMO_CASES.md` query cases | Pending |

## Final Regression Notes

Implementation for all P1 stages is present in source files and documentation. Final database replay is still required in an environment with a reachable MySQL service and either a MySQL client or an equivalent schema import path.
