import os
import json

# API requests 
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT'))  # sec

# Base URL Binance API
BINANCE_API_BASE = os.getenv('BINANCE_API_BASE')
PRICE_URL = os.getenv('PRICE_URL')

#DB
DB_DSN = os.getenv('DB_DSN')

#Portfolio data
PORTFOLIO = json.loads(os.getenv('PORTFOLIO'))

#Others
CLEAN_BATCH_SIZE = int(os.getenv('CLEAN_BATCH_SIZE'))