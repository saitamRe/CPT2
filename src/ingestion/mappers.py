from src.dto.portfolio_dto import PortfolioSnapshot, AssetDetails, PortfolioLogRow
from decimal import Decimal

def portfolio_to_rows(snap: PortfolioSnapshot[str, AssetDetails]) -> list[PortfolioLogRow]:
    """Converts a portfolio snapshot into a list of log rows, one per asset."""
    
    return [
        PortfolioLogRow(
            snap['timestamp'],
            sym,
            Decimal(item['price']),
            Decimal(item['quantity']),
            Decimal(item['amount'])
        )
        for sym, item in snap['asset_details'].items()
    ]