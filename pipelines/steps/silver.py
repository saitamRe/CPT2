import logging
import time

import psycopg

from db.layers.silver.silver_builder import rebuild_silver

logger = logging.getLogger(__name__)

def run(conn):
    t0 = time.perf_counter()
    logger.info('silver step start')

    try:  
        
        rebuild_silver(conn)
        logger.info('silver step end', extra={
            'status': 'success',
            'duration_ms': int((time.perf_counter() - t0)*1000)
        })  
    except psycopg.Error:
        logger.exception('silver step end', extra={
            'status': 'fail',
            'duration_ms': int((time.perf_counter() - t0)*1000)
        })
        raise
    

