# P1 Acceptance Checklist

This checklist tracks P1 requirements, implementation targets, verification steps, and final acceptance status. It assumes a clean database created from `schema.sql` before full regression.

## Scope

| Requirement | Target | Verification | Status | Notes |
| --- | --- | --- | --- | --- |
| P1-DATA-001 | `/data/students` | Page shows student number, name, phone, and status for all students. | Pending | Stage 02 |
| P1-DATA-002 | `/data/shops` | Page shows shop ID, shop name, campus location, and status for all shops. | Pending | Stage 02 |
| P1-DATA-003 | `/data/drinks` | Page shows drink ID, shop name, drink name, price, stock, and status; stock change is visible after adding an order. | Pending | Stage 03 |
| P1-DATA-004 | `/data/coupons` | Page shows coupon ID, student name, amount, minimum order amount, validity date, and status; coupon status change is visible after adding an order. | Pending | Stage 03 |
| P1-FORM-001 | `/order/add` | Student selection is a database-backed dropdown showing student name and number. | Pending | Stage 04 |
| P1-FORM-002 | `/order/add` | Group order selection is a database-backed dropdown showing title and ID, with `OPEN` orders first. | Pending | Stage 04 |
| P1-FORM-003 | `/order/add` | Drink selection is a database-backed dropdown showing drink name, price, and stock. | Pending | Stage 04 |
| P1-FORM-004 | `/order/add` | Coupon selection is a database-backed dropdown showing coupon name and amount, supports no coupon, and lists `UNUSED` coupons first. | Pending | Stage 04 |
| P1-ERR-001 | P0 operation pages | Database trigger, procedure, and transaction errors are displayed as user-readable page messages without stack traces. | Pending | Stage 05 |
| P1-ERR-002 | `/order/add` | Required fields are checked and quantity must be a positive integer. | Pending | Stage 05 |
| P1-LOG-001 | `operation_logs` | Successful add order writes `ADD_ORDER_ITEM` with student ID, group order ID, and drink ID. | Pending | Stage 06 |
| P1-LOG-002 | `operation_logs` | Successful finish group writes `FINISH_GROUP_ORDER` with group order ID and total amount. | Pending | Stage 06 |
| P1-LOG-003 | `operation_logs` | Successful cancel group writes `CANCEL_GROUP_ORDER` with group order ID. | Pending | Stage 06 |
| P1-LOG-004 | `/logs` | Page shows operation type, detail, and time in reverse chronological order. | Pending | Stage 07 |
| P1-DEMO-001 | `/` | Homepage shows quick entries for add order, finish group, cancel group, and group detail query. | Pending | Stage 08 |
| P1-DEMO-002 | `/` | Homepage shows student count, shop count, drink count, open group count, and finished group count. | Pending | Stage 08 |

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

Final P1 regression should update this section with the actual database replay result, page smoke result, P0 workflow result, P1 workflow result, and any remaining environment limits.
