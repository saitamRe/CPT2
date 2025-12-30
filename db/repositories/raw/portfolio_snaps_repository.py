from src.domain.portfolio_types import PortfolioSnapshot, AssetDetails
import psycopg
from typing import Iterable

upsert_sql = """
    INSERT INTO raw.portfolio_logs(timestamp, symbol, price, quantity, amount)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT(timestamp, symbol)
    DO UPDATE SET(
        price = EXCLUDED.price,
        quantity = EXCLUDED.quantity,
        amount = EXCLUDED.amount
    )
"""

def save_snapshot_to_db(conn: psycopg.Connection, snap: PortfolioSnapshot[str, AssetDetails]):
    rows = _portfolio_to_rows(snap)
    with conn.cursor() as cur:
        cur.executemany(upsert_sql, rows)

def _portfolio_to_rows(snap: PortfolioSnapshot[str, AssetDetails]) -> Iterable[tuple[str, str, float, float , float]]:

    for sym, item in snap.items():
        yield(
            snap['timestamp'],
            sym,
            item['price'],
            item['quantity'],
            item['amount']
        )
