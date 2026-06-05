DROP DATABASE IF EXISTS milk_tea_group_db;
CREATE DATABASE milk_tea_group_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE milk_tea_group_db;
SET NAMES utf8mb4;

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

DELIMITER //

CREATE TRIGGER trg_before_order_item_insert
BEFORE INSERT ON order_items
FOR EACH ROW
BEGIN
    DECLARE v_student_count INT DEFAULT 0;
    DECLARE v_student_status VARCHAR(16);
    DECLARE v_group_count INT DEFAULT 0;
    DECLARE v_group_shop_id INT;
    DECLARE v_group_status VARCHAR(16);
    DECLARE v_drink_count INT DEFAULT 0;
    DECLARE v_drink_shop_id INT;
    DECLARE v_drink_price DECIMAL(10, 2);
    DECLARE v_drink_stock INT;
    DECLARE v_drink_status VARCHAR(16);
    DECLARE v_coupon_count INT DEFAULT 0;
    DECLARE v_coupon_student_id INT;
    DECLARE v_coupon_amount DECIMAL(10, 2) DEFAULT 0.00;
    DECLARE v_coupon_min_amount DECIMAL(10, 2) DEFAULT 0.00;
    DECLARE v_coupon_valid_until DATE;
    DECLARE v_coupon_status VARCHAR(16);

    IF NEW.quantity <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '购买数量必须大于0';
    END IF;

    SELECT COUNT(*), MAX(status)
    INTO v_student_count, v_student_status
    FROM students
    WHERE student_id = NEW.student_id;

    IF v_student_count = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '学生不存在，不能下单';
    END IF;

    IF v_student_status <> 'ACTIVE' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '学生状态异常，不能下单';
    END IF;

    SELECT COUNT(*), MAX(shop_id), MAX(status)
    INTO v_group_count, v_group_shop_id, v_group_status
    FROM group_orders
    WHERE group_order_id = NEW.group_order_id;

    IF v_group_count = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '拼单不存在，不能下单';
    END IF;

    IF v_group_status <> 'OPEN' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '拼单不是进行中状态，不能下单';
    END IF;

    SELECT COUNT(*), MAX(shop_id), MAX(price), MAX(stock), MAX(status)
    INTO v_drink_count, v_drink_shop_id, v_drink_price, v_drink_stock, v_drink_status
    FROM drinks
    WHERE drink_id = NEW.drink_id;

    IF v_drink_count = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '饮品不存在，不能下单';
    END IF;

    IF v_drink_status <> 'ON_SALE' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '饮品不是在售状态，不能下单';
    END IF;

    IF v_drink_shop_id <> v_group_shop_id THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '饮品不属于该拼单店铺，不能下单';
    END IF;

    IF v_drink_stock < NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '饮品库存不足，不能下单';
    END IF;

    SET NEW.item_amount = v_drink_price * NEW.quantity;
    SET NEW.discount_amount = 0.00;

    IF NEW.coupon_id IS NOT NULL THEN
        SELECT
            COUNT(*),
            MAX(student_id),
            MAX(amount),
            MAX(min_order_amount),
            MAX(valid_until),
            MAX(status)
        INTO
            v_coupon_count,
            v_coupon_student_id,
            v_coupon_amount,
            v_coupon_min_amount,
            v_coupon_valid_until,
            v_coupon_status
        FROM coupons
        WHERE coupon_id = NEW.coupon_id;

        IF v_coupon_count = 0 THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '优惠券不存在，不能下单';
        END IF;

        IF v_coupon_student_id <> NEW.student_id THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '优惠券不属于当前学生，不能下单';
        END IF;

        IF v_coupon_status <> 'UNUSED' THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '优惠券不是未使用状态，不能下单';
        END IF;

        IF v_coupon_valid_until < CURRENT_DATE THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '优惠券已过期，不能下单';
        END IF;

        IF NEW.item_amount < v_coupon_min_amount THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '订单金额未达到优惠券最低使用金额';
        END IF;

        IF v_coupon_amount > NEW.item_amount THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '优惠金额不能大于订单原价';
        END IF;

        SET NEW.discount_amount = v_coupon_amount;
    END IF;

    SET NEW.pay_amount = NEW.item_amount - NEW.discount_amount;
    SET NEW.status = 'CREATED';

    UPDATE drinks
    SET stock = stock - NEW.quantity
    WHERE drink_id = NEW.drink_id;

    IF NEW.coupon_id IS NOT NULL THEN
        UPDATE coupons
        SET status = 'USED'
        WHERE coupon_id = NEW.coupon_id;
    END IF;

    INSERT INTO operation_logs (op_type, detail)
    VALUES (
        'ADD_ORDER',
        CONCAT(
            'student_id=', NEW.student_id,
            ', group_order_id=', NEW.group_order_id,
            ', drink_id=', NEW.drink_id,
            ', quantity=', NEW.quantity
        )
    );
END//

DELIMITER ;
