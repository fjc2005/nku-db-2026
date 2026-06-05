# P0 Demo Cases

This file records stable demo inputs after rebuilding the database with `schema.sql`.
Run the cases in the listed order for a full P0 walkthrough, or rebuild the database
before repeating an individual case.

## Reset

1. Execute `schema.sql` in MySQL.
2. Start the Flask app.
3. Open `/` and confirm the homepage loads.

## 1. Trigger Success: Add Order

Page: `/order/add`

Input:

| Field | Value |
| --- | --- |
| group_order_id | 1 |
| student_id | 1 |
| drink_id | 1 |
| quantity | 1 |
| coupon_id | 1 |

Expected result:

- Page shows `加入拼单成功`.
- A new `order_items` row is created.
- Drink `1` stock decreases by `1`.
- Coupon `1` changes to `USED`.

## 2. Trigger Failure: Locked Student

Page: `/order/add`

Input:

| Field | Value |
| --- | --- |
| group_order_id | 1 |
| student_id | 3 |
| drink_id | 1 |
| quantity | 1 |
| coupon_id | Leave empty |

Expected result:

- Page shows `学生状态异常，不能下单`.
- No new `order_items` row is created.
- Drink stock and coupon state remain unchanged.

## 3. Stored Procedure Success: Finish Group

Page: `/group/finish`

Input:

| Field | Value |
| --- | --- |
| group_order_id | 2 |

Expected result:

- Page shows `拼单完成成功`.
- Group order `2` changes to `FINISHED`.
- Its order item changes to `PAID`.
- Group order `2` total amount becomes `15.00`.

## 4. Stored Procedure Failure: Repeat Finish

Page: `/group/finish`

Input:

| Field | Value |
| --- | --- |
| group_order_id | 2 |

Expected result:

- Page shows `拼单不是进行中状态，不能完成`.
- Group order `2` and its order item remain unchanged after the failed repeat.

## 5. Transaction Failure: Finished Group

Page: `/group/cancel`

Input:

| Field | Value |
| --- | --- |
| group_order_id | 3 |

Expected result:

- Page shows `已完成拼单不能取消`.
- Group order `3` and its order item remain unchanged.
- Drink stock and coupon state remain unchanged.

## 6. Transaction Success: Cancel Group

Page: `/group/cancel`

Input:

| Field | Value |
| --- | --- |
| group_order_id | 5 |

Expected result:

- Page shows `取消拼单成功`.
- Group order `5` is deleted.
- Its order item is deleted.
- Drink `1` stock increases by `1`.
- Coupon `5` changes to `UNUSED`.

## 7. View Query

Page: `/group/query`

Useful inputs:

| Case | group_order_id | student_name | group_status |
| --- | --- | --- | --- |
| Query finished detail | 3 | Leave empty | FINISHED |
| Query by student | Leave empty | Zhang | Leave empty |
| Query canceled detail | Leave empty | Leave empty | CANCELED |

Expected result:

- Results are read from `v_group_order_detail`.
- Rows include student, shop, drink, group order, and order item fields.
- CANCELED status returns the seeded historical canceled detail for group order `4`.

## P1 Demo Route

Run this section after rebuilding the database with `schema.sql`. It can follow the
P0 walkthrough, but for the clearest screenshots use a fresh reset first.

### 1. Homepage Dashboard

Page: `/`

Expected result:

- The page shows the four scoring operation entries: add order, finish group, cancel group, and group detail query.
- The page shows five statistic cards: students, shops, drinks, open group orders, and finished group orders.
- With the seed data, the initial counts are 4 students, 2 shops, 5 drinks, 3 open group orders, and 1 finished group order.

### 2. Basic Data Pages

Pages:

| Page | Path | Screenshot focus |
| --- | --- | --- |
| Students | `/data/students` | Student number, name, phone, status |
| Shops | `/data/shops` | Shop ID, name, campus location, status |
| Drinks | `/data/drinks` | Drink ID, shop name, drink name, price, stock, status |
| Coupons | `/data/coupons` | Coupon ID, student name, amount, minimum order amount, validity date, status |

Expected result:

- All rows come from the database seed data.
- The drinks and coupons pages can be refreshed after adding an order to show inventory and coupon status changes.

### 3. Dropdown Add Order

Page: `/order/add`

Recommended input:

| Field | Value |
| --- | --- |
| group order | `1` |
| student | `1` |
| drink | `1` |
| quantity | `1` |
| coupon | `1` |

Expected result:

- The form uses dropdowns for group order, student, drink, and coupon.
- Page shows `加入拼单成功`.
- `/data/drinks` shows drink `1` stock decreased by `1`.
- `/data/coupons` shows coupon `1` changed to `USED`.
- `/logs` includes an `ADD_ORDER_ITEM` row containing `student_id=1`, `group_order_id=1`, and `drink_id=1`.

Optional no-coupon case:

| Field | Value |
| --- | --- |
| group order | `1` |
| student | `2` |
| drink | `2` |
| quantity | `1` |
| coupon | No coupon |

Expected result:

- Page shows `加入拼单成功`.
- The created order item has discount amount `0.00`.

### 4. Validation And Friendly Errors

Pages: `/order/add`, `/group/finish`, `/group/cancel`

Useful checks:

| Case | Expected result |
| --- | --- |
| Submit add order with missing required fields | Page shows the missing field message |
| Submit quantity `0`, a negative number, or non-numeric text | Page shows a quantity or number format message |
| Submit locked student `3` on add order | Page shows `学生状态异常，不能下单` |
| Finish group order `2` twice | The repeat attempt shows `拼单不是进行中状态，不能完成` |
| Cancel finished group order `3` | Page shows `已完成拼单不能取消` and data remains unchanged |

### 5. Operation Logs

Page: `/logs`

Recommended success operations:

1. Add order with the first dropdown demo case.
2. Finish group order `2`.
3. Cancel group order `5`.

Expected result:

- The page shows `ADD_ORDER_ITEM`, `FINISH_GROUP_ORDER`, and `CANCEL_GROUP_ORDER`.
- Logs are sorted by operation time descending.
- Failed operations do not create success log rows.
