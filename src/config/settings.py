from pathlib import Path

PROJECT_ROOT =  Path(__file__).resolve().parents[2]

# Base URL Binance API
BINANCE_API_BASE = "https://data-api.binance.vision"
PRICE_URL = '/api/v3/ticker/price'

PORTFOLIO = {
    'BTC': 0.57,
    'ETH': 14.0,
    'APT': 54.0
}