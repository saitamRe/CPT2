from typing import TypedDict, NamedTuple, Any
from decimal import Decimal
from datetime import datetime

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

