import logging

import psycopg

from db.repositories.raw.portfolio_logs_repository import save_snapshot_to_db
from src.config.settings import settings
from src.dto.portfolio_dto import PortfolioLogRow
from src.errors.data_quality import DataQualityError
from src.ingestion.fetcher import PortfolioFetcher
from src.ingestion.mappers import portfolio_to_rows
from src.quality import runner
from src.quality.checks.raw_checks import (
    check_decimal_finite_non_negative,
    check_symbol_str_and_non_empty,
    check_timestamp_utc_or_naive,
)
from src.quality.logger import log_quality_report
from src.quality.policy import CheckSpec, Severity

logger = logging.getLogger(__name__)

RAW_SPECS = [
    CheckSpec('symbol_str_and_non_empty', Severity.FAIL, check_symbol_str_and_non_empty),
    CheckSpec('decimal_finite_non_negative', Severity.FAIL, check_decimal_finite_non_negative),
    CheckSpec('timestamp_utc_or_naive', Severity.FAIL, check_timestamp_utc_or_naive)
]

def _fetch_rows() -> list[PortfolioLogRow]:
    fetcher = PortfolioFetcher(settings.portfolio)
    snap = fetcher.get_portfolio_value()
    return portfolio_to_rows(snap)

def run(conn: psycopg.Connection) -> None:
    """Fetch portfolio snapshot, run DQ checks, and persist to raw layer."""
    rows = _fetch_rows()
    report = runner.run_raw_quality_checks('raw.portfolio_logs', rows, RAW_SPECS)
    log_quality_report(logger, report, step='ingestion', layer='raw')
    if not report.passed:
        failed_checks = [r.name for r in report.failed(Severity.FAIL)]
        raise DataQualityError(
            f'Ingestion quality failed for raw.portfolio_logs {failed_checks}'
            )
    save_snapshot_to_db(conn, rows)

 