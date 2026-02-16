from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid

from src.dto.portfolio_dto import PortfolioLogRow
from src.quality.policy import CheckSpec, Severity

from .checks.raw_checks import CheckResult


@dataclass(frozen=True)
class QualityReport:
    dataset: str
    run_id: str
    created_at: datetime
    results: list[CheckResult]
    specs: list[CheckSpec]

    @property
    def passed(self) -> bool:
        sev = {s.name: s.severity for s in self.specs}
        return all(r.passed and sev.get(r.name) == Severity.FAIL for r in self.results)

    def failed(self, severity_type: Severity) -> list[PortfolioLogRow]:
        sev = {s.name: s.severity for s in self.specs}  

        return [r for r in self.results if (not r.passed and sev.get(r.name) == severity_type)]

        

def run_raw_quality_checks(dataset: str, rows: list[PortfolioLogRow], specs: list[CheckSpec]) -> QualityReport:
    results: list[CheckResult] = []

    for s in specs:
        r = s.fn(rows)

        if r.name != s.name:
            r = CheckResult(name=s.name, passed=r.passed, stats=r.stats, samples=r.samples, message=r.message)
        results.append(r)


    return QualityReport(
        dataset=dataset,
        run_id=str(uuid.uuid4()),
        created_at=datetime.now(tz=timezone.utc),
        results=results,
        specs=specs
    )



