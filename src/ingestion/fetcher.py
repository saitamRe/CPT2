from src.api.binance_client import BinanceClient
from datetime import datetime, timezone
from src.dto.portfolio_dto import PortfolioSnapshot, AssetDetails
from decimal import Decimal
from src.config.settings import settings



class PortfolioFetcher:
    def __init__(self, portfolio: dict):
        self.portfolio = portfolio
        self.client = BinanceClient(settings.binance_api_base, settings.price_url, settings.request_timeout)
    
    def get_portfolio_value(self) -> PortfolioSnapshot[str, AssetDetails]:
        
        asset_details = {}

        for symbol, quantity in self.portfolio.items():

            coin_price = Decimal(self.client.get_price(f'{symbol}usdt'))
            quantity = Decimal(quantity)
            amount = coin_price * quantity

            asset_details[symbol] = {
                'price': Decimal(coin_price),
                'quantity': Decimal(quantity), 
                'amount': Decimal(amount)
            }

        snap: PortfolioSnapshot = {
            'timestamp': datetime.now(timezone.utc),
            'asset_details': asset_details
        }

        return snap
        