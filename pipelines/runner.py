import time
import logging
from dotenv import load_dotenv
from db.init.schema import get_db, ensure_db_schema
from pipelines.steps import clean, gold, ingestion, silver
from src.config.logger_config import (
     get_new_run_id,
     set_pipeline,
     set_run_id,
     set_step,
     setup_logging,
)

load_dotenv()

logger = logging.getLogger(__name__)

    
def main() -> None:
    setup_logging()
    set_pipeline('cpt_etl')
    set_run_id(get_new_run_id())

    t0 = time.perf_counter()
    logger.info('pipeline_start')

    try:
        with get_db() as conn:  
           ensure_db_schema(conn)

        set_step('ingestion')
        with get_db() as conn:
            with conn.transaction():
                ingestion.run(conn)
        
        set_step('clean')
        with get_db() as conn:
            with conn.transaction():
                clean.run(conn)
        
        set_step('silver')
        with get_db() as conn:
            with conn.transaction():
                silver.run(conn)

        set_step('gold')
        with get_db() as conn:
            with conn.transaction():
                gold.run(conn)

        logger.info('pipeline_end', extra={
            'status': 'success',
            'duration_ms': int((time.perf_counter() - t0)*1000)
            })
    except Exception:
        logger.exception('pipeline_end', extra= {
            'status':'failed',
            'duration_ms':int((time.perf_counter() - t0)*1000),
        }, )
        raise
    


if __name__ == '__main__':
    main()
