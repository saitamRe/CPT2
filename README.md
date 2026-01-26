# Crypto portfolio tracker (ETL)
ETL pipeline that collect, clean, transform, aggreagate and store data received from Binance API 


## Overview
This project is built to practice Data Engineering fundamentals:
- building reliable ETL pipeline
- working with PostgreeSQL
- applying Medallion architecture(raw -> clean -> silver -> gold)
- writing idemponent and debuggable data pipeline

## Data Flow
1. Fetch portfolio snapshot from Binance API
2. Store raw data 
3. Clean the data
4. Aggregate the data
5. Store final data sets in gold layer

## Tech Stack
- Python
- PostgreeSQL
- psycopg
- Docker(planned)

## How to Run
1. Create virtual environment
2. Install dependencies:
   pip install -r requirements.txt
3. Set environment variables:
   DB_DSN=...
4. Run pipeline:
   "module": "pipelines.runner"