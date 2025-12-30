import psycopg
from pathlib import Path
from src.config.settings import PROJECT_ROOT

def read_sql_file(conn: psycopg.Connection, p: Path) -> str:
    if not p.exists():
        return
    return p.read_text(p)

def execute_script(conn: psycopg.Connection, sql: str) -> None:
    sql = (sql or '').strip()
    if not sql:
        return
    with conn.cursor() as cur:
        cur.execute(sql)

def execute_dir(conn: psycopg.Connection, layer: str, dir: str) -> None:
    root = PROJECT_ROOT / layer / dir
    
    if not root.exists():
        return

    for p in sorted(root.glob('*.sql')):
        execute_script(conn, read_sql_file(p))

def ensure_raw(conn: psycopg.Connection) -> None:
    execute_dir(conn, 'raw', 'tables')
    execute_dir(conn, 'raw', 'views')
    execute_dir(conn, 'raw', 'indexes')

def execute_schemas(conn: psycopg.Connection) -> None:
    execute_script(conn, 'db/init/01_init_schemas.sql')

def ensure_all(conn: psycopg.Connection) -> None:
    ensure_raw(conn)