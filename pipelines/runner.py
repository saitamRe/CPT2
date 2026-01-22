import logging
import time
from pipelines.steps import ingestion, clean
from db.init.schema import get_db, ensure_all
from src.config.logger_config import set_pipeline, set_run_id, set_step, setup_logging, get_new_run_id

logger = logging.getLogger(__name__)
    
def main() -> None:
    setup_logging()
    set_pipeline('cpt_etl')
    set_run_id(get_new_run_id())

    t0 = time.perf_counter()
    logger.info('pipeline_start')

    try:
        with get_db() as conn:
            with conn:
                ensure_all(conn)

                set_step('ingestion')
                ingestion.run(conn)
                
                set_step('clean')
                clean.run(conn)
    except Exception:
        logger.exception('pipeline_end', extra= {
            'status':'failed',
            'duration_ms':int((time.perf_counter() - t0)),
        }, )
        raise
    


if __name__ == '__main__':
    main()
