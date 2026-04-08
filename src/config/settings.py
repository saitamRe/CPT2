import os
import json

from src.utils.retry import RetryConfig

#TODO _required func to validate presense of var's values. if not - exception

# API requests 
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT'))  # sec

BINANCE_RETRY_CONFIG = RetryConfig(
    max_attempts = 3,
    base_delay = 0.5,
    max_delay = 5,
    backoff_factor = 2,
    jitter = 0.1,
    retry_exceptions=(TimeoutError, ConnectionError)
)

# Base URL Binance API
BINANCE_API_BASE = os.getenv('BINANCE_API_BASE')
PRICE_URL = os.getenv('PRICE_URL')

#DB
DB_DSN = os.getenv('DB_DSN')

#Portfolio data
#Q json loads - principle of working
PORTFOLIO = json.loads(os.getenv('PORTFOLIO'))

#Others
CLEAN_BATCH_SIZE = int(os.getenv('CLEAN_BATCH_SIZE'))

