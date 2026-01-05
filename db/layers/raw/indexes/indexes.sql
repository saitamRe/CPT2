CREATE UNIQUE INDEX IF NOT EXISTS idx_portfolio_logs_ts_symbol
ON raw.portfolio_logs(timestamp, symbol);


