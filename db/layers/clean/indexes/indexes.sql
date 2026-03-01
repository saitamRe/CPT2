
CREATE UNIQUE INDEX IF NOT EXISTS idx_clean_assets_ts_symbol
ON clean.assets(timestamp, symbol);

