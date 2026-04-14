import psycopg
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Iterator
from src.config.settings import settings

DB_ROOT_LAYERS =  Path(__file__).resolve().parents[1] / 'layers'

def read_sql_file(p: Path) -> str:
    if not p.exists():
        return
    return p.read_text('utf-8')

def execute_script(conn: psycopg.Connection, sql: str) -> None:
    sql = (sql or '').strip()
    if not sql:
        return
    with conn.cursor() as cur:
        cur.execute(sql)

def execute_dir(conn, layer: str, dir: str) -> None:
    root = DB_ROOT_LAYERS / layer / dir
    
    if not root.exists():
        return

    for p in sorted(root.glob('*.sql')):
        execute_script(conn, read_sql_file(p))

def ensure_raw(conn) -> None:
    execute_dir(conn, 'raw', 'tables')
    execute_dir(conn, 'raw', 'views')
    execute_dir(conn, 'raw', 'indexes')

def ensure_clean(conn) -> None:
    execute_dir(conn, 'clean', 'tables')
    execute_dir(conn, 'clean', 'views')
    execute_dir(conn, 'clean', 'indexes')

def ensure_silver(conn):
    execute_dir(conn, 'silver', 'tables')
    execute_dir(conn, 'silver', 'indexes')
    execute_dir(conn, 'silver', 'views')

def ensure_gold(conn):
    execute_dir(conn, 'gold', 'tables')
    execute_dir(conn, 'gold', 'indexes')
    execute_dir(conn, 'gold', 'views')

def ensure_meta(conn):
    execute_dir(conn, 'meta', 'tables')

def execute_schemas(conn) -> None:
    execute_script(conn, read_sql_file(Path('db/init/01_init_schemas.sql')))

def ensure_all(conn) -> None:
    ensure_raw(conn)
    ensure_clean(conn)
    ensure_silver(conn)
    ensure_gold(conn)
    ensure_meta(conn)

@contextmanager
def get_db(dsn: Optional[str] = None) -> Iterator[psycopg.Connection]:
    conn = psycopg.connect(dsn or settings.db_dsn)
    try:
        yield conn
    finally:
        conn.close() 

