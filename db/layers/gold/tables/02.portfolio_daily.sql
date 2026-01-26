CREATE TABLE IF NOT EXISTS gold.portfolio_daily(
    date DATE PRIMARY KEY,
    last_ts TIMESTAMP NOT NULL,
    amount NUMERIC(18,8) NOT NULL
)