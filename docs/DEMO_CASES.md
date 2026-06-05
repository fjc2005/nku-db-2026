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
