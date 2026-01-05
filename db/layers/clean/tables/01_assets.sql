
CREATE TABLE IF NOT EXISTS clean.assets(
    timestamp TIMESTAMP NOT NULL,
    symbol TEXT NOT NULL,
    price NUMERIC(18, 8),
    quantity NUMERIC(18, 8),
    amount NUMERIC(18, 8)
);