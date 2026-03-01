import psycopg
import logging
import time
from db.repositories.clean import assets_repository
from db.repositories.raw import portfolio_logs_repository
from src.cleaning.cleaner import clean_batch
from src.config.settings import CLEAN_BATCH_SIZE
from src.etl_meta.steps import PipelineSteps
from db.repositories.watermarks.watermarks_repository import Watermark, get_watermark, update_wm
from src.dto.portfolio_dto import raw_row_to_log_raw

logger = logging.getLogger(__name__)



def run(conn: psycopg.Connection):
    t0 = time.perf_counter()
    logger.info('clean step start')

    rows_read = 0

    try:
        wm = get_watermark(conn, step=PipelineSteps.CLEAN)
        while True:
            with conn.transaction():
                
                raw_rows_batch = portfolio_logs_repository.get_snapshots_after_wm(conn, wm, CLEAN_BATCH_SIZE)
                if not raw_rows_batch:
                    break
                log_rows_batch = [raw_row_to_log_raw(row) for row in raw_rows_batch]

                clean_rows = clean_batch(log_rows_batch)
                assets_repository.upsert_batch(conn, clean_rows)
                new_wm = Watermark(raw_rows_batch[-1].timestamp, raw_rows_batch[-1].id)
                update_wm(conn, PipelineSteps.CLEAN, new_wm)
            rows_read += len(raw_rows_batch)
            wm = new_wm
        clean_timer = time.perf_counter()
        logger.info('clean_step_end', extra={
            'status': 'success',
            'duration_ms': int((time.perf_counter() - clean_timer)*1000),
            'rows_read': rows_read
        })
    except (psycopg.Error, ValueError, TypeError):
        logger.exception('step_end', extra=
                    {
                    'status': 'failed',
                    'duration_ms': int((time.perf_counter() - t0)*1000),
                    'rows_read': rows_read,
                    },
                    )
        raise

    