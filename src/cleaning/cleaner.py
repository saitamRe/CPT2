import re
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from src.dto.portfolio_dto import PortfolioLogRow


#TODO remake according to the injestion layer changes
#Remove checks which are not appropriate for this layer. For example 
#inf validation should be on raw layer
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


def clean_batch(log_rows: list[PortfolioLogRow]) -> list[CleanAssetRow]:
    return [
        CleanAssetRow(
            timestamp=_ensure_ts(row.timestamp),
            symbol=_norm_symbol(row.symbol),
            price=_ensure_decimal(row.price, 'price'),
            quantity=_ensure_decimal(row.quantity, 'quantity'),
            amount=_ensure_decimal(row.amount, 'amount')
        )
        for row in log_rows
    ]


def iter_clean_portfolio_snapshot(snapshots):
    """Compatibility wrapper around clean_batch for streaming use."""
    for row in snapshots:
        yield from clean_batch([row])
             

