# Crypto Portfolio Tracker (ETL)

![CI](https:/saitamRe/github.com/CPT2/actions/workflows/ci.yml/badge.svg)

ETL pipeline that fetches, validates, transforms, and aggregates crypto portfolio data from the Binance API using a Medallion architecture.

---

## Architecture

```mermaid
flowchart LR
    A[Binance API] -->|fetch prices| B[raw.portfolio_logs]
    B -->|keyset pagination\n+ DQ checks| C[clean.assets]
    C --> D[silver.asset_snapshot\nsilver.portfolio_totals]
    D --> E[gold.asset_daily\ngold.portfolio_daily]
```

---

## Data Flow

| Layer | Table(s) | Description |
|-------|----------|-------------|
| **Raw** | `raw.portfolio_logs` | Stores data as received from API. Minimal structural validation. |
| **Clean** | `clean.assets` | Validated and normalized rows. DQ checks with FAIL/WARN severity. |
| **Silver** | `silver.asset_snapshot`, `silver.portfolio_totals` | Aggregated snapshots and portfolio totals over time. |
| **Gold** | `gold.asset_daily`, `gold.portfolio_daily` | Final daily aggregates ready for analytics. |

---

## Key Design Decisions

- **Keyset pagination** in the clean step: reads raw data in bounded batches using `(timestamp, id)` cursor. Avoids OFFSET performance degradation on large tables.
- **Transaction per batch**: each batch is committed independently. On failure, already-committed batches are preserved and the pipeline can resume from the last watermark.
- **Watermark tracking**: the `meta.watermarks` table stores the last processed `(timestamp, id)` per step, enabling reliable incremental processing.
- **Data Quality checks**: raw rows are validated before persistence. Failed checks with `FAIL` severity stop the pipeline; `WARN` severity is logged only.
- **Retry with exponential backoff**: Binance API calls are retried automatically on network errors with configurable delay and jitter.

---

## Data Quality

**Dataset:** `raw.portfolio_logs`  
**Grain:** 1 row = portfolio snapshot for `(timestamp, symbol)`

| Check | Severity | Description |
|-------|----------|-------------|
| Symbol not blank | FAIL | Symbol must be a non-empty string |
| Decimal finite and non-negative | FAIL | price, quantity, amount must be valid Decimals |
| Timestamp is datetime | FAIL | timestamp must be a datetime instance |

---

## Tech Stack

- Python 3.11+
- PostgreSQL
- psycopg (v3)
- Docker + Docker Compose


---

## Project Structure

```
pipelines/          # Pipeline runner and steps
src/
  api/              # Binance API client
  cleaning/         # Validation and normalization logic
  ingestion/        # Fetcher, mappers
  quality/          # DQ checks, report, severity policy
  utils/            # Retry logic
  etl_meta/         # Watermark model
db/
  layers/           # SQL: tables, indexes, views per layer
  repositories/     # Data access per layer
tests/              # Unit tests
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_DSN` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/cpt2` |
| `BINANCE_API_BASE` | Binance API base URL | `https://data-api.binance.vision` |
| `PRICE_URL` | Price endpoint path | `/api/v3/ticker/price` |
| `PORTFOLIO` | JSON map of symbol to quantity | `{"BTC": "0.1", "ETH": "1.0"}` |
| `REQUEST_TIMEOUT` | API request timeout in seconds | `10` |
| `CLEAN_BATCH_SIZE` | Rows per batch in clean step | `2000` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## How to Run

```bash
cp .env.example .env
# Fill in PORTFOLIO and other values in .env
docker-compose up
```
