CREATE DATABASE IF NOT EXISTS momo_analytics;

USE momo_analytics;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE transaction_categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);


CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(15,2) NOT NULL,
    transaction_time DATETIME NOT NULL,
    processed_by VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    category_id INT NOT NULL,

    CONSTRAINT chk_transaction_amount
        CHECK (amount > 0),

    CONSTRAINT chk_transaction_status
        CHECK (status IN ('SUCCESS', 'PENDING', 'FAILED')),

    CONSTRAINT fk_transaction_category
        FOREIGN KEY (category_id)
        REFERENCES transaction_categories(category_id)
);


CREATE TABLE transaction_participants (
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    role VARCHAR(20) NOT NULL,

    PRIMARY KEY (transaction_id, user_id),

    CONSTRAINT fk_participant_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_participant_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_participant_role
        CHECK (role IN ('SENDER', 'RECEIVER'))
);


CREATE TABLE system_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    log_message VARCHAR(255) NOT NULL,
    log_level VARCHAR(20) NOT NULL,
    log_time DATETIME NOT NULL,

    CONSTRAINT fk_log_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_log_level
        CHECK (log_level IN ('INFO', 'WARNING', 'ERROR'))
);


CREATE INDEX idx_users_phone
    ON users(phone_number);

CREATE INDEX idx_transactions_time
    ON transactions(transaction_time);

CREATE INDEX idx_transactions_category
    ON transactions(category_id);

CREATE INDEX idx_transactions_status
    ON transactions(status);

CREATE INDEX idx_participants_user
    ON transaction_participants(user_id);

CREATE INDEX idx_logs_transaction
    ON system_logs(transaction_id);

CREATE INDEX idx_logs_level
    ON system_logs(log_level);


INSERT INTO users (phone_number, name)
VALUES
('0788000001', 'Jean Claude'),
('0788000002', 'Aline Mukamana'),
('0788000003', 'Eric Niyonzima'),
('0788000004', 'Grace Uwase'),
('0788000005', 'Samuel Habimana');


INSERT INTO transaction_categories (category_name, description)
VALUES
('TRANSFER', 'Money transferred between users'),
('PAYMENT', 'Payment for goods or services'),
('AIRTIME', 'Purchase of airtime'),
('WITHDRAWAL', 'Money withdrawn from an account'),
('DEPOSIT', 'Money deposited into an account');


INSERT INTO transactions
    (amount, transaction_time, processed_by, status, category_id)
VALUES
(5000.00, '2026-09-10 08:30:00', 'System', 'SUCCESS', 1),
(12500.00, '2026-09-10 09:15:00', 'System', 'SUCCESS', 2),
(2000.00, '2026-09-10 10:00:00', 'System', 'SUCCESS', 3),
(30000.00, '2026-09-10 11:45:00', 'System', 'PENDING', 4),
(15000.00, '2026-09-10 13:20:00', 'System', 'FAILED', 5);

INSERT INTO transaction_participants
    (transaction_id, user_id, role)
VALUES
(1, 1, 'SENDER'),
(1, 2, 'RECEIVER'),

(2, 2, 'SENDER'),
(2, 3, 'RECEIVER'),

(3, 3, 'SENDER'),
(3, 4, 'RECEIVER'),

(4, 4, 'SENDER'),
(4, 5, 'RECEIVER'),

(5, 5, 'SENDER'),
(5, 1, 'RECEIVER');


-- ----------------------------
-- SYSTEM LOGS
-- ----------------------------

INSERT INTO system_logs
    (transaction_id, log_message, log_level, log_time)
VALUES
(1, 'Transaction processed successfully', 'INFO', '2026-09-10 08:30:05'),
(2, 'Payment transaction completed', 'INFO', '2026-09-10 09:15:05'),
(3, 'Airtime purchase completed', 'INFO', '2026-09-10 10:00:05'),
(4, 'Transaction is awaiting processing', 'WARNING', '2026-09-10 11:45:05'),
(5, 'Transaction processing failed', 'ERROR', '2026-09-10 13:20:05');

SELECT * FROM users;
SELECT * FROM transaction_categories;
SELECT * FROM transactions;
SELECT * FROM transaction_participants;
SELECT * FROM system_logs;

SELECT
    t.transaction_id,
    t.amount,
    t.transaction_time,
    t.status,
    tc.category_name
FROM transactions t
JOIN transaction_categories tc
    ON t.category_id = tc.category_id;

INSERT INTO users (phone_number, name)
VALUES ('0788999999', 'Test User');

SELECT *
FROM users
WHERE phone_number = '0788999999';

UPDATE users
SET name = 'Updated Test User'
WHERE phone_number = '0788999999';

SELECT *
FROM users
WHERE phone_number = '0788999999';

DELETE FROM users
WHERE phone_number = '0788999999';

SELECT *
FROM users
WHERE phone_number = '0788999999';