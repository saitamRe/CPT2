from datetime import datetime, timezone
from typing import Any, Iterator
import re
from decimal import Decimal, InvalidOperation
from dataclasses import dataclass
from src.dto.portfolio_dto import PortfolioLogRow

@dataclass
class CleanAssetRow:
    timestamp: str
    symbol: str
    price: Decimal
    quantity: Decimal
    amount: Decimal


_SYMBOL_RE = re.compile(r'^[A-Z0-9_-]+$')

#contract - naive dt-s are treated as utc ones
def _dt_to_iso_utc(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt= dt.astimezone(timezone.utc)
    return dt.replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def _parse_ts(ts: Any) -> datetime:
    if isinstance(ts, datetime):
        return ts
    
    if not isinstance(ts, str):
        raise ValueError(f'Input should be either datetime or str, got {type(ts)}')
    
    s = ts.strip()
    if s.endswith('z', 'Z'):
        s = s[:-1] + '+00:00'
    
    try:
        return datetime.fromisoformat(s)
    except ValueError as e:
        raise ValueError(f'Error while ts parsing. Input value was {ts!r}')
    
def _norm_symbol(sym: str) -> str:
    if not isinstance(sym, str):
        raise TypeError(f'Input should be the str type, got {sym!r}')
    
    s = sym.strip().upper()

    if not s:
        raise ValueError('Empty symbol')
    
    if not _SYMBOL_RE.fullmatch(s):
        raise ValueError(f'Invalid symbol: {s!r}')
    
    return s

def _parse_decimal(n: Any, name: str) -> Decimal:
    if isinstance(n, float):
        raise ValueError(f'{name} should be decimal, got {n!r}')
    try:
        v = Decimal(n)
    except (InvalidOperation, TypeError):
        raise ValueError(f'{name} should be a valid number, got {n!r}')
    if not v.is_finite():
        raise ValueError(f'{name} should be finite, got {v!r}')  
    if v < 0:
        raise ValueError(f'{name} should be non-negative, got {v!r}')
    return v

def iter_clean_portfolio_snapshot(snapshots: list[PortfolioLogRow]) -> Iterator[CleanAssetRow]:
    
    for snap in snapshots:
        yield CleanAssetRow(
            timestamp=_dt_to_iso_utc(_parse_ts(snap.timestamp)),
            symbol=_norm_symbol(snap.symbol),
            price=_parse_decimal(snap.price, 'price'),
            quantity=_parse_decimal(snap.quantity, 'quantity'),
            amount=_parse_decimal(snap.amount, 'amount')
        )
       
    
    