
CREATE TABLE IF NOT EXISTS bank_transactions (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(30),
    account_number VARCHAR(30),
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(10) NOT NULL
        CHECK (transaction_type IN ('Debit', 'Credit')),
    category VARCHAR(100),
    merchant VARCHAR(200),
    description TEXT,
    amount NUMERIC(15, 2) NOT NULL
        CHECK (amount > 0),
    balance NUMERIC(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT * FROM bank_transactions;

select current_user;
ALTER ROLE postgres WITH PASSWORD 'Op@123';

