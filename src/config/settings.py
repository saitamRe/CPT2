from pathlib import Path

# API requests 
REQUEST_TIMEOUT = 10  # sec

# Base URL Binance API
BINANCE_API_BASE = "https://data-api.binance.vision"
PRICE_URL = '/api/v3/ticker/price'

#DB
DB_DSN = 'postgresql://postgres:050695@localhost:5432/cpt2'

PORTFOLIO = {
    'BTC': 0.57,
    'ETH': 14.0,
    'APT': 54.0
}

CLEAN_BATCH_SIZE = 2000