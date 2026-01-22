import psycopg
import logging
import time
from db.repositories.clean import assets_repository
from db.repositories.raw import portfolio_logs_repository
from src.cleaning import cleaner
from src.common.core.iterators import batch
from src.config.settings import CLEAN_BATCH_SIZE

logger = logging.getLogger(__name__)

def run(conn: psycopg.Connection):
    t0 = time.perf_counter()
    logger.info('step start')

    rows_read = 0

    try:
        max_ts = assets_repository.get_max_ts(conn)
        if max_ts is not None:
            data = portfolio_logs_repository.iter_snapshots_after(conn, max_ts)
        else:
            data = portfolio_logs_repository.iter_all_snapshots(conn)
        clean_data = cleaner.iter_clean_portfolio_snapshot(data)

        for one_batch in batch(clean_data, CLEAN_BATCH_SIZE):
            bt = time.perf_counter()
            n = len(one_batch)
            rows_read += n
            assets_repository.upsert_batch(conn, one_batch)
            logger.info('batch upsert ok', 
                        extra={
                            'duration_ms':int((time.perf_counter() - bt)*1000),
                            'batch_len':n,
                            'rows_read':rows_read
                        }
                        )
    except Exception:
        logger.info('step_end', extra=
                    {
                    'status': 'failed',
                    'duration_ms': int((time.perf_counter() - t0)*1000),
                    'rows_read': rows_read,
                    },
                    )
        raise

    