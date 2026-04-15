import logging
import time

import psycopg

from db.repositories.clean import assets_repository
from db.repositories.raw import portfolio_logs_repository
from db.repositories.watermarks.watermarks_repository import Watermark, get_watermark, update_wm
from src.cleaning.cleaner import clean_batch
from src.config.settings import settings
from src.dto.portfolio_dto import raw_row_to_log_raw
from src.etl_meta.steps import PipelineSteps

logger = logging.getLogger(__name__)



def run(conn: psycopg.Connection):
    t0 = time.perf_counter()
    logger.info('clean step start')

    rows_read = 0

    try:
        #better to call it via repo. Review all the module to fix that
        wm = get_watermark(conn, step=PipelineSteps.CLEAN)
        while True:
            with conn.transaction():
                
                raw_rows_batch = portfolio_logs_repository.get_snapshots_after_wm(
                    conn, 
                    wm, 
                    settings.clean_batch_size
                    )
                if not raw_rows_batch:
                    logger.info('no new data for clean', extra={'wm': wm})
                    break
                log_rows_batch = [raw_row_to_log_raw(row) for row in raw_rows_batch]

                clean_rows = clean_batch(log_rows_batch)
                assets_repository.upsert_batch(conn, clean_rows)
                new_wm = Watermark(raw_rows_batch[-1].timestamp, raw_rows_batch[-1].id)
                update_wm(conn, PipelineSteps.CLEAN, new_wm)
                rows_read += len(raw_rows_batch)
                wm = new_wm
        logger.info('clean_step_end', extra={
            'status': 'success',
            'duration_ms': int((time.perf_counter() - t0)*1000),
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

    