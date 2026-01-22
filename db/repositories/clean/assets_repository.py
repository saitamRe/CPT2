import psycopg
from datetime import datetime
from src.cleaning.cleaner import CleanAssetRow

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

def upsert_batch(conn: psycopg.Connection, cleaned_batch: list[CleanAssetRow]) -> None:

    rows = [
        ( row.timestamp,
            row.symbol,
            row.price,
            row.quantity,
            row.amount,
        )
        for row in cleaned_batch
    ]
    with conn.cursor() as cur:
        cur.executemany(_UPSERT_SQL, rows)
    

def get_max_ts(conn: psycopg.Connection) -> datetime | None:
    with conn.cursor() as cur:
        cur.execute(_GET_MAX_SQL)
        t = cur.fetchone()
    return t[0] if t else None
