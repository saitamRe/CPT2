
CREATE TABLE IF NOT EXISTS raw.portfolio_logs(
    id BIGINT GENERATED ALWAYS AS IDENTITY, 
    timestamp TIMESTAMP NOT NULL,
    symbol TEXT NOT NULL,
    price NUMERIC(18, 8),
    quantity NUMERIC(18, 8),
    amount NUMERIC(18, 8)
)