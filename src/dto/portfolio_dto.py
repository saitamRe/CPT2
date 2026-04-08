from typing import TypedDict, NamedTuple
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass


class AssetDetails(TypedDict):
    price: Decimal
    quantity: Decimal
    amount: Decimal

class PortfolioSnapshot(TypedDict):
    timestamp: datetime
    asset_details: dict[str, AssetDetails]

class PortfolioLogRow(NamedTuple):
    timestamp: datetime
    symbol: str
    price: Decimal
    quantity: Decimal
    amount: Decimal

@dataclass
class RawPortfolioLogRow:
    id: int #Q do we need id here
    timestamp: datetime
    symbol: str
    price: Decimal
    quantity: Decimal
    amount: Decimal

#Q is it ok to have this method in the DTO module? i dont know also if we really need rawrow and logrow
def raw_row_to_log_raw(row: RawPortfolioLogRow) -> PortfolioLogRow:
    return PortfolioLogRow(
        timestamp=row.timestamp,
        symbol=row.symbol,
        price=row.price,
        quantity=row.quantity,
        amount=row.amount
    )
