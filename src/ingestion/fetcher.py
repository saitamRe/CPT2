from src.api.binance_client import BinanceClient
from datetime import datetime, timezone
from src.domain.portfolio_types import PortfolioSnapshot, AssetDetails

class PortfolioFetcher:
    def __init__(self, portfolio: dict):
        self.portfolio = portfolio
        self.client = BinanceClient()
    
    def get_portfolio_value(self) -> PortfolioSnapshot[str, AssetDetails]:
        
        asset_details = {}

        for symbol, quantity in self.portfolio.items():

            coin_price = self.client.get_price(symbol)
            amount = coin_price * quantity

            asset_details[symbol] = {
                'price': float(coin_price),
                'quantity': float(quantity), 
                'amount': float(amount)
            }

        snap: PortfolioSnapshot = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'asset_details': asset_details
        }

        return snap
        