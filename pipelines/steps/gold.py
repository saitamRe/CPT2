import logging
import time

import psycopg

from db.layers.gold.gold_builder import rebuild_gold

logger = logging.getLogger(__name__)

def run(conn):
    t0 = time.perf_counter()
    logger.info('gold_step_start')

    try:
        rebuild_gold(conn)
        logger.info('gold_step_end', extra={
            'status': 'success',
            'duration_ms': int((time.perf_counter() - t0)*1000)
        })
    except psycopg.Error:
        logger.exception('gold_step_end', extra={
            'status': 'failed',
            'duration_ms': int((time.perf_counter()- t0)*1000)
        })
        raise