from psycopg import Connection
import logging

from src.config import settings
from db.repositories.raw.portfolio_logs_repository import save_snapshot_to_db
from src.dto.portfolio_dto import PortfolioLogRow
from src.errors.data_quality import DataQualityError
from src.ingestion.mappers import iter_portfolio_to_rows
from src.ingestion.fetcher import PortfolioFetcher
from src.quality import runner
from src.quality.policy import CheckSpec, Severity
from src.quality.checks.raw_checks import(
    check_decimal_finite_non_negative,
    check_symbol_str_and_non_empty,
    check_timestamp_utc_or_naive
)
from src.quality.logger import log_quality_report

logger = logging.getLogger(__name__)

#TODO do we need to store specs here?
RAW_SPECS = [
    CheckSpec('symbol_str_and_non_empty', Severity.FAIL, check_symbol_str_and_non_empty),
    CheckSpec('decimal_finite_non_negative', Severity.FAIL, check_decimal_finite_non_negative),
    CheckSpec('timestamp_utc_or_naive', Severity.FAIL, check_timestamp_utc_or_naive)
]

def fetch_rows():
    fetcher = PortfolioFetcher(settings.PORTFOLIO)
    snap = fetcher.get_portfolio_value()
    #TODO seems like after the refactoring i dont need iterator here anymore
    return list(iter_portfolio_to_rows(snap))

def run(conn: Connection, rows: list[PortfolioLogRow]):
    #TODO 'runner' name is confusing. Need to be changed
    report = runner.run_raw_quality_checks('raw.portfolio_logs', rows, RAW_SPECS)
    log_quality_report(logger, report, step='ingestion', layer='raw')
    if not report.passed:
        raise DataQualityError(f'Ingestion quality failed for raw.portfolio_logs {[r.name for r in report.failed(Severity.FAIL)]}')
    save_snapshot_to_db(conn, rows)

 