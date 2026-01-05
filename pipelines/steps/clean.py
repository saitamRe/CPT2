import psycopg
from db.repositories.clean import assets_repository
from db.repositories.raw import portfolio_logs_repository
from src.cleaning import cleaner
from src.common.core.iterators import batch
from src.config.settings import CLEAN_BATCH_SIZE

def run(conn: psycopg.Connection):
    max_ts = assets_repository.get_max_ts(conn)
    if max_ts is not None:
        data = portfolio_logs_repository.iter_snapshots_after(conn, max_ts)
    else:
        data = portfolio_logs_repository.iter_all_snapshots(conn)
    clean_data = cleaner.iter_clean_portfolio_snapshot(data)

    for one_batch in batch(clean_data, CLEAN_BATCH_SIZE):
        assets_repository.upsert_many(conn, one_batch)

    