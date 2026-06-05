DROP DATABASE IF EXISTS milk_tea_group_db;
CREATE DATABASE milk_tea_group_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE milk_tea_group_db;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_no VARCHAR(32) NOT NULL,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_students_student_no UNIQUE (student_no),
    CONSTRAINT chk_students_status CHECK (status IN ('ACTIVE', 'LOCKED'))
) ENGINE=InnoDB;

CREATE TABLE shops (
    shop_id INT AUTO_INCREMENT PRIMARY KEY,
    shop_name VARCHAR(100) NOT NULL,
    campus_location VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(16) NOT NULL DEFAULT 'OPEN',
    CONSTRAINT chk_shops_status CHECK (status IN ('OPEN', 'CLOSED'))
) ENGINE=InnoDB;

CREATE TABLE drinks (
    drink_id INT AUTO_INCREMENT PRIMARY KEY,
    shop_id INT NOT NULL,
    drink_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    status VARCHAR(16) NOT NULL DEFAULT 'ON_SALE',
    CONSTRAINT chk_drinks_price CHECK (price > 0),
    CONSTRAINT chk_drinks_stock CHECK (stock >= 0),
    CONSTRAINT chk_drinks_status CHECK (status IN ('ON_SALE', 'OFF_SALE')),
    CONSTRAINT fk_drinks_shop
        FOREIGN KEY (shop_id) REFERENCES shops (shop_id)
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE group_orders (
    group_order_id INT AUTO_INCREMENT PRIMARY KEY,
    shop_id INT NOT NULL,
    creator_student_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    deadline_at DATETIME NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'OPEN',
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_group_orders_status CHECK (status IN ('OPEN', 'FINISHED', 'CANCELED')),
    CONSTRAINT chk_group_orders_total_amount CHECK (total_amount >= 0),
    CONSTRAINT fk_group_orders_shop
        FOREIGN KEY (shop_id) REFERENCES shops (shop_id)
        ON UPDATE CASCADE,
    CONSTRAINT fk_group_orders_creator
        FOREIGN KEY (creator_student_id) REFERENCES students (student_id)
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE coupons (
    coupon_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    coupon_name VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    min_order_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    valid_until DATE NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'UNUSED',
    CONSTRAINT chk_coupons_amount CHECK (amount > 0),
    CONSTRAINT chk_coupons_min_order_amount CHECK (min_order_amount >= 0),
    CONSTRAINT chk_coupons_status CHECK (status IN ('UNUSED', 'USED')),
    CONSTRAINT fk_coupons_student
        FOREIGN KEY (student_id) REFERENCES students (student_id)
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    group_order_id INT NOT NULL,
    student_id INT NOT NULL,
    drink_id INT NOT NULL,
    coupon_id INT NULL,
    quantity INT NOT NULL,
    item_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    pay_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(16) NOT NULL DEFAULT 'CREATED',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_order_items_quantity CHECK (quantity > 0),
    CONSTRAINT chk_order_items_item_amount CHECK (item_amount >= 0),
    CONSTRAINT chk_order_items_discount_amount CHECK (discount_amount >= 0),
    CONSTRAINT chk_order_items_pay_amount CHECK (pay_amount >= 0),
    CONSTRAINT chk_order_items_status CHECK (status IN ('CREATED', 'PAID', 'CANCELED')),
    CONSTRAINT fk_order_items_group_order
        FOREIGN KEY (group_order_id) REFERENCES group_orders (group_order_id)
        ON UPDATE CASCADE,
    CONSTRAINT fk_order_items_student
        FOREIGN KEY (student_id) REFERENCES students (student_id)
        ON UPDATE CASCADE,
    CONSTRAINT fk_order_items_drink
        FOREIGN KEY (drink_id) REFERENCES drinks (drink_id)
        ON UPDATE CASCADE,
    CONSTRAINT fk_order_items_coupon
        FOREIGN KEY (coupon_id) REFERENCES coupons (coupon_id)
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE operation_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    op_type VARCHAR(50) NOT NULL,
    detail VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT INTO students (student_id, student_no, name, phone, status) VALUES
    (1, 'S2026001', 'Zhang Ming', '18800000001', 'ACTIVE'),
    (2, 'S2026002', 'Li Na', '18800000002', 'ACTIVE'),
    (3, 'S2026003', 'Wang Lei', '18800000003', 'LOCKED'),
    (4, 'S2026004', 'Chen Yu', '18800000004', 'ACTIVE');

INSERT INTO shops (shop_id, shop_name, campus_location, phone, status) VALUES
    (1, 'Tea Campus East', 'East Cafeteria 1F', '02100000001', 'OPEN'),
    (2, 'Fruit Tea Lab', 'West Life Plaza', '02100000002', 'CLOSED');

INSERT INTO drinks (drink_id, shop_id, drink_name, price, stock, status) VALUES
    (1, 1, 'Pearl Milk Tea', 12.00, 37, 'ON_SALE'),
    (2, 1, 'Taro Bobo Milk', 15.00, 19, 'ON_SALE'),
    (3, 1, 'Lemon Green Tea', 10.00, 0, 'ON_SALE'),
    (4, 1, 'Matcha Latte', 16.00, 8, 'OFF_SALE'),
    (5, 2, 'Full Fruit Tea', 18.00, 25, 'ON_SALE');

INSERT INTO group_orders (
    group_order_id,
    shop_id,
    creator_student_id,
    title,
    deadline_at,
    status,
    total_amount
) VALUES
    (1, 1, 1, 'East Lunch Group Order', DATE_ADD(NOW(), INTERVAL 4 HOUR), 'OPEN', 0.00),
    (2, 1, 2, 'Study Room Group Order', DATE_ADD(NOW(), INTERVAL 6 HOUR), 'OPEN', 0.00),
    (3, 1, 1, 'Finished Demo Group Order', DATE_SUB(NOW(), INTERVAL 1 DAY), 'FINISHED', 24.00),
    (4, 1, 1, 'Canceled Demo Group Order', DATE_SUB(NOW(), INTERVAL 2 DAY), 'CANCELED', 0.00),
    (5, 1, 4, 'Cancel Transaction Demo', DATE_ADD(NOW(), INTERVAL 8 HOUR), 'OPEN', 0.00);

INSERT INTO coupons (
    coupon_id,
    student_id,
    coupon_name,
    amount,
    min_order_amount,
    valid_until,
    status
) VALUES
    (1, 1, 'New Student Discount', 2.00, 10.00, DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), 'UNUSED'),
    (2, 2, 'Used Club Coupon', 3.00, 15.00, DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), 'USED'),
    (3, 3, 'Locked Student Coupon', 2.00, 10.00, DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), 'UNUSED'),
    (4, 1, 'Expired Demo Coupon', 2.00, 10.00, DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY), 'UNUSED'),
    (5, 2, 'Cancel Restore Coupon', 4.00, 10.00, DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), 'USED');

INSERT INTO order_items (
    order_item_id,
    group_order_id,
    student_id,
    drink_id,
    coupon_id,
    quantity,
    item_amount,
    discount_amount,
    pay_amount,
    status
) VALUES
    (1, 2, 2, 2, NULL, 1, 15.00, 0.00, 15.00, 'CREATED'),
    (2, 3, 1, 1, NULL, 2, 24.00, 0.00, 24.00, 'PAID'),
    (3, 5, 2, 1, 5, 1, 12.00, 4.00, 8.00, 'CREATED');

INSERT INTO operation_logs (log_id, op_type, detail) VALUES
    (1, 'INIT_SCHEMA', 'Seed data initialized for P0 database demos.');
