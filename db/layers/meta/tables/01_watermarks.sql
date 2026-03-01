
CREATE TABLE IF NOT EXISTS meta.watermarks(
    step TEXT PRIMARY KEY,
    last_ts TIMESTAMP NOT NULL,
    last_id BIGINT NOT NULL, 
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
 
INSERT INTO meta.watermarks(step, last_ts, last_id)
VALUES ('clean_assets', '1970-01-01 00:00:00', 0)
ON CONFLICT (step) DO NOTHING