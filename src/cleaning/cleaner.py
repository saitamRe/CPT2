from datetime import datetime, timezone
from typing import Any, Iterator
import re
from decimal import Decimal
from dataclasses import dataclass
from src.dto.portfolio_dto import PortfolioLogRow

#TODO remake according to the injestion layer changes
#Remove checks which are not appropriate for this layer. For example inf validation should be on raw layer
@dataclass
class CleanAssetRow:
    timestamp: datetime
    symbol: str
    price: Decimal
    quantity: Decimal
    amount: Decimal


_SYMBOL_RE = re.compile(r'^[A-Z0-9_-]+$')


def _ensure_ts(ts: Any) -> datetime:
    if isinstance(ts, datetime):
        if not ts.tzinfo:
            ts = ts.replace(tzinfo=timezone.utc)
        else:
            ts = ts.astimezone(timezone.utc)
        return ts
    raise TypeError(f'ts must be datetime, got {type(ts)}')
    
def _norm_symbol(sym: Any) -> str:
    if not isinstance(sym, str):
        raise TypeError(f'Input should be the str type, got {sym!r}')
    
    s = sym.strip().upper()

    if not s:
        raise ValueError('Empty symbol')
    
    if not _SYMBOL_RE.fullmatch(s):
        raise ValueError(f'Invalid symbol: {s!r}')
    
    return s

def _ensure_decimal(n: Any, name: str) -> Decimal:
    if isinstance(n, float):
        raise TypeError(f'float type isnt allowed for {name}, got {n!r}')

    if not isinstance(n, Decimal):
        raise TypeError(f'{name} should be decimal, got {type(n).__name__}')
   
    if not n.is_finite():
        raise ValueError(f'{name} should be finite, got {n!r}')  
    if n < 0:
        raise ValueError(f'{name} should be non-negative, got {n!r}')
    return n

def iter_clean_portfolio_snapshot(snapshots: Iterator[PortfolioLogRow]) -> Iterator[CleanAssetRow]:
    """Lazily normalize raw portfolio snapshots.

    This is a generator: it validates and converts each input row and yields
    CleanAssetRow one by one (no buffering into a list).

    Rules enforced:
    - timestamp must be timezone-aware UTC datetime (naive is assumed UTC)
    - symbol is stripped, uppercased, and validated against allowed pattern
    - price/quantity/amount must be finite, non-negative Decimals (floats are rejected)

    Args:
        snapshots: Iterator of raw portfolio log rows.

    Yields:
        CleanAssetRow with normalized and validated fields.
    """
    for snap in snapshots:
        yield CleanAssetRow(
            timestamp=_ensure_ts(snap.timestamp),
            symbol=_norm_symbol(snap.symbol),
            price=_ensure_decimal(snap.price, 'price'),
            quantity=_ensure_decimal(snap.quantity, 'quantity'),
            amount=_ensure_decimal(snap.amount, 'amount')
        ) 