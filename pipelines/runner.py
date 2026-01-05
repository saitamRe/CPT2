from pipelines.steps import ingestion, clean
from db.init.schema import get_db, ensure_all

    
def main():
    with get_db() as conn:
        with conn:
            ensure_all(conn)
            ingestion.run(conn)
            clean.run(conn)
    


if __name__ == '__main__':
    main()
