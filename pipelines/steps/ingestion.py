from psycopg import Connection
from src.ingestion.fetcher import PortfolioFetcher
from src.config import settings
from db.repositories.raw.portfolio_logs_repository import save_snapshot_to_db

def run(conn: Connection):
    fetcher = PortfolioFetcher(settings.PORTFOLIO)
    snap = fetcher.get_portfolio_value()
    save_snapshot_to_db(conn, snap)