from typing import TypedDict
from decimal import Decimal

class AssetDetails(TypedDict):
    price: Decimal
    quantity: Decimal
    amount: Decimal

class PortfolioSnapshot(TypedDict):
    timestamp: str
    asset_details: dict[str, AssetDetails]