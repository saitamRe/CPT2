from dataclasses import dataclass
from enum import Enum
from typing import Callable

from src.dto.portfolio_dto import PortfolioLogRow
from src.quality.checks.raw_checks import CheckResult

class Severity(str, Enum):
    FAIL = 'FAIL'
    WARN = 'WARN'
    LOG = 'LOG'

@dataclass(frozen=True)
class CheckSpec:
    name: str
    severity: Severity
    fn: Callable[[list[PortfolioLogRow]], CheckResult]

