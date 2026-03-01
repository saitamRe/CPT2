import psycopg
from datetime import datetime, timezone
from dataclasses import dataclass
from src.etl_meta.steps import PipelineSteps

_UPSERT_WATERMARK_SQL = """
    INSERT INTO meta.watermarks(step, last_ts, last_id, updated_at)
    VALUES(%s, %s, %s, %s)
    ON CONFLICT(step) DO UPDATE
        SET
        last_ts = EXCLUDED.last_ts,
        last_id = EXCLUDED.last_id,
        updated_at = EXCLUDED.updated_at
"""

_GET_WATERMARK_SQL = """
    SELECT last_ts, last_id
    FROM meta.watermarks
    WHERE step = %(step)s
    FOR UPDATE
"""

@dataclass
class Watermark:
    last_ts: datetime
    last_id: int

def update_wm(conn: psycopg.Connection, step: PipelineSteps, wm: Watermark):
    with conn.cursor() as cur:
        cur.execute(_UPSERT_WATERMARK_SQL, (step, wm.last_ts, wm.last_id, datetime.now(timezone.utc)))


def get_watermark(conn: psycopg.Connection, step: str) -> tuple[datetime, int]:
    with conn.cursor() as cur:
        cur.execute(
            _GET_WATERMARK_SQL, 
            {'step': step}
        )
        ts, id = cur.fetchone()
        return Watermark(ts, id)