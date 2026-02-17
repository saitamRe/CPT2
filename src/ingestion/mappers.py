from typing import Iterator
from src.dto.portfolio_dto import PortfolioSnapshot, AssetDetails, PortfolioLogRow
from decimal import Decimal

def iter_portfolio_to_rows(snap: PortfolioSnapshot[str, AssetDetails]) -> Iterator[PortfolioLogRow]:
    """
    Convert a portfolio snapshot into an iterator of log rows for persistence.

    This function flattens the `asset_details` mapping from the snapshot into
    one `PortfolioLogRow` per asset, carrying over the snapshot timestamp and
    converting all numeric fields to `Decimal`. It does not perform any
    validation; callers are responsible for ensuring the snapshot is wellformed.

    Args:
        snap: In-memory portfolio snapshot with a single timestamp and a mapping
            from asset symbol to its price, quantity, and amount.

    Yields:
        PortfolioLogRow instances, one per asset in the snapshot.
    """
    for sym, item in snap['asset_details'].items():
        yield PortfolioLogRow(
            snap['timestamp'],
            sym,
            Decimal(item['price']),
            Decimal(item['quantity']),
            Decimal(item['amount'])
        )