CREATE TABLE IF NOT EXISTS silver.asset_snapshot(
    timestamp TIMESTAMP NOT NULL,
    symbol TEXT NOT NULL,
    price NUMERIC(18, 8) NOT NULL,
    quantity NUMERIC(18, 8) NOT NULL,
    amount NUMERIC(18, 8) NOT NULL,
    PRIMARY KEY(symbol, timestamp)
)