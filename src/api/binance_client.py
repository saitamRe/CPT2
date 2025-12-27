import requests
from src.errors.api import BinanceApiError

class BinanceClient:
    def __init__(self, base_url, price_url, timeout):
        self.base_url = base_url
        self.price_url = price_url
        self.timeout = timeout
    
    def get_price(self, symbol:str) -> float:
        symbol = symbol.strip().upper()
        if not symbol:
            raise ValueError('Symbol is empty')

        try:
            response = requests.get(
                f'{self.base_url}{self.price_url}',
                params={'symbol': symbol.strip().upper()},
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return float(data['price'])
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            raise BinanceApiError(f'Binance API error: {e}') from e

        