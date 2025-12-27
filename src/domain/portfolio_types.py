from typing import TypedDict

class AssetDetails(TypedDict):
    price: float
    quantity: float
    amount: float

class PortfolioSnapshot(TypedDict):
    timestamp: str
    asset_details: dict[str, AssetDetails]