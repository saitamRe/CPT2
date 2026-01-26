CREATE TABLE IF NOT EXISTS gold.asset_daily(
    date DATE NOT NULL,
    symbol TEXT NOT NULL,
    quantity_end NUMERIC(18,8) NOT NULL,
    amount_end NUMERIC(18,8) NOT NULL,
    PRIMARY KEY (date, symbol)
)