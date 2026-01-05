from datetime import datetime, timezone
from typing import Any
from decimal import Decimal, InvalidOperation
import re

_SYM_RE = re.compile(r'^[A-Z0-9_-]+$') 

def _ts_to_iso_utc(ts: datetime) -> str:
    if not ts.tzinfo:
        dt = ts.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    
    return dt.replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def _parse_ts(ts: Any) -> datetime:
    if isinstance(ts, datetime):
        return ts
    
    if not isinstance(ts, str):
        raise TypeError(f'Ts should be either datetime or str type. Got {ts!r}')
    
    s = ts.strip()

    if not s:
        raise ValueError(f'Empty input')
    
    if s.endswith('z', 'Z'):
        s = s[:-1] + '+00:00'
    
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        raise ValueError(f'Parsing failed. Got {s!r}')

def _parse_decimal(n: Any, name: str) -> Decimal:
    if isinstance(n, float):
        raise ValueError(f'{name} cant be float. Got {n!r}')

    try:
        v = Decimal(n)
    except (InvalidOperation, TypeError):
        raise ValueError(f'Error parsing {name} value. Got f{n!r}')
    
    if not v.is_finite():
        raise ValueError(f'{name} should be finite. Got {v!r}')
    
    return v

def _norm_symbol(sym: str) -> str:   
    if not isinstance(sym, str):
        raise ValueError(f'Symbol should be a str. Got {sym!r}')

    s = sym.strip().upper() 

    if not s:
        raise ValueError(f'Empty input')
    
    if not _SYM_RE.fullmatch(s):
        raise ValueError(f'Invalid symbol. Got {s!r}')
    
    return s