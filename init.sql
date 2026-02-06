CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    amount FLOAT,
    user_id INT,
    merchant_id INT,
    is_anomaly BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);