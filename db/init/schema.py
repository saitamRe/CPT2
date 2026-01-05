import psycopg
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Iterator
from src.config.settings import DB_DSN

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

def execute_dir(conn: psycopg.Connection, layer: str, dir: str) -> None:
    root = DB_ROOT_LAYERS / layer / dir
    
    if not root.exists():
        return

    for p in sorted(root.glob('*.sql')):
        execute_script(conn, read_sql_file(p))

def ensure_raw(conn: psycopg.Connection) -> None:
    execute_dir(conn, 'raw', 'tables')
    execute_dir(conn, 'raw', 'views')
    execute_dir(conn, 'raw', 'indexes')

def ensure_clean(conn: psycopg.Connection) -> None:
    execute_dir(conn, 'clean', 'tables')
    execute_dir(conn, 'clean', 'views')
    execute_dir(conn, 'clean', 'indexes')

def execute_schemas(conn: psycopg.Connection) -> None:
    execute_script(conn, read_sql_file(Path('db/init/01_init_schemas.sql')))

def ensure_all(conn: psycopg.Connection) -> None:
    ensure_raw(conn)
    ensure_clean(conn)

@contextmanager
def get_db(dsn: Optional[str] = None) -> Iterator[psycopg.Connection]:
    conn = psycopg.connect(dsn or DB_DSN)
    try:
        yield conn
    finally:
        conn.close() 

