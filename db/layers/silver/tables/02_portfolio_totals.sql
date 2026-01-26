CREATE TABLE IF NOT EXISTS silver.portfolio_totals(
    timestamp TIMESTAMP NOT NULL PRIMARY KEY,
    amount NUMERIC(18, 8) NOT NULL
)