import logging
import requests
from src.config.settings import settings
from src.errors.api import BinanceApiError
from decimal import Decimal

from src.utils.retry import run_with_retry

logger = logging.getLogger(__name__)

class BinanceClient:
    def __init__(self, base_url, price_url, timeout):
        self.base_url = base_url
        self.price_url = price_url
        self.timeout = timeout
    
    def get_price(self, symbol: str):
        return run_with_retry(
            self._get_price_impl,
            step_name='binance_get_request',
            logger=logger,
            config=settings.binance_retry_config,
            symbol=symbol
            )

    def _get_price_impl(self, symbol:str) -> float:
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
            return Decimal(data['price'])
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            raise BinanceApiError(f'Binance API error: {e}') from e

        