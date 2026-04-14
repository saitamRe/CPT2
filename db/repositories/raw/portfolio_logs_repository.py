import psycopg

from src.dto.portfolio_dto import RawPortfolioLogRow

from src.dto.portfolio_dto import PortfolioLogRow
from db.repositories.watermarks.watermarks_repository import Watermark

_UPSERT_SQL = """
    INSERT INTO raw.portfolio_logs(timestamp, symbol, price, quantity, amount)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT(timestamp, symbol)
    DO UPDATE SET
        price = EXCLUDED.price,
        quantity = EXCLUDED.quantity,
        amount = EXCLUDED.amount
"""

_GET_AFTER_WM_SQL = """
    SELECT id, timestamp, symbol, price, quantity, amount 
    FROM raw.portfolio_logs
    WHERE (timestamp, id) > (%(last_ts)s, %(last_id)s)
    ORDER BY timestamp, id
    LIMIT %(batch_size)s
"""



def save_snapshot_to_db(conn: psycopg.Connection, rows: list[PortfolioLogRow]) -> None:
    """Upsert a batch of portfolio log rows into raw.portfolio_logs."""
    if not len(rows):
        raise ValueError('Portfolio should contain at least one row')
    with conn.cursor() as cur:
        cur.executemany(_UPSERT_SQL, rows)


def get_snapshots_after_wm(conn: psycopg.Connection, wm: Watermark, batch_size: int) -> list[RawPortfolioLogRow]:
    """
    Fetch a paginated batch of raw portfolio rows after the given watermark.

    Uses keyset pagination on (timestamp, id) for stable ordering. The caller
    is responsible for computing the next watermark from the last row in the
    batch.

    Args:
        conn: Database connection.
        wm: Watermark (last_ts, last_id) from the previous batch.
        batch_size: Maximum number of rows to return.

    Returns:
        List of raw portfolio rows including id. Empty if no rows remain.
    """
    with conn.cursor() as cur:
        cur.execute(_GET_AFTER_WM_SQL, {'last_ts': wm.last_ts, 'last_id': wm.last_id, 'batch_size': batch_size})
        raw_rows = cur.fetchall()
        return [RawPortfolioLogRow(*row) for row in raw_rows]



