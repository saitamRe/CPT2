import psycopg
from datetime import datetime
from src.dto.portfolio_dto import PortfolioLogRow

_GET_MAX_SQL = """
    SELECT MAX(timestamp)
    FROM clean.assets
"""

_UPSERT_SQL = """
    INSERT INTO clean.assets(timestamp, symbol, price, quantity, amount)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT(timestamp, symbol) DO UPDATE 
        SET
        price = EXCLUDED.price,
        quantity = EXCLUDED.quantity,
        amount = EXCLUDED.amount
    
"""

def upsert_many(conn: psycopg.Connection, cleaned_snaps: list[PortfolioLogRow]) -> None:
    with conn.cursor() as cur:
        cur.executemany(_UPSERT_SQL, cleaned_snaps)
    

def get_max_ts(conn: psycopg.Connection) -> datetime | None:
    with conn.cursor() as cur:
        cur.execute(_GET_MAX_SQL)
        t = cur.fetchone()
    return t[0] if t else None
