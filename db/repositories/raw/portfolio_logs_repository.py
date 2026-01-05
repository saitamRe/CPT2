from src.dto.portfolio_dto import PortfolioSnapshot, AssetDetails, PortfolioLogRow
import psycopg
from typing import Iterable, Iterator
from decimal import Decimal
from datetime import datetime

_UPSERT_SQL = """
    INSERT INTO raw.portfolio_logs(timestamp, symbol, price, quantity, amount)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT(timestamp, symbol)
    DO UPDATE SET
        price = EXCLUDED.price,
        quantity = EXCLUDED.quantity,
        amount = EXCLUDED.amount
"""

_GET_AFTER_SQL = """
    SELECT timestamp, symbol, price, quantity, amount
    FROM raw.portfolio_logs
    WHERE timestamp >= %s
    ORDER BY timestamp, symbol
"""

_GET_ALL_SQL = """
    SELECT timestamp, symbol, price, quantity, amount FROM raw.portfolio_logs
"""

def save_snapshot_to_db(conn: psycopg.Connection, snap: PortfolioSnapshot[str, AssetDetails]):
    rows = list(_portfolio_to_rows(snap))

    if not len(rows):
        raise ValueError('Portfolio should contain at least one row')

    with conn.cursor() as cur:
        cur.executemany(_UPSERT_SQL, rows)

def _portfolio_to_rows(snap: PortfolioSnapshot[str, AssetDetails]) -> Iterable[PortfolioLogRow]:

    for sym, item in snap['asset_details'].items():
        yield(
            snap['timestamp'],
            sym,
            Decimal(item['price']),
            Decimal(item['quantity']),
            Decimal(item['amount'])
        )


def iter_snapshots_after(conn: psycopg.Connection, ts: datetime) -> Iterator[PortfolioLogRow]:
    with conn.cursor() as cur:
        cur.execute(_GET_AFTER_SQL, (ts, ))
        for row in cur:
            yield PortfolioLogRow(*row)

def iter_all_snapshots(conn: psycopg.Connection) -> Iterator[PortfolioLogRow]:
    with conn.cursor() as cur:
        cur.execute(_GET_ALL_SQL)
        for row in cur:
            yield PortfolioLogRow(*row)
