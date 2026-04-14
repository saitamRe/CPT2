from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid

from src.dto.portfolio_dto import PortfolioLogRow
from src.quality.policy import CheckSpec, Severity

from .checks.raw_checks import CheckResult

#Soon. we need to get rid from attachment to the PortfolioLogRow here. Ticket is created

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
        return all(r.passed for r in self.results if sev.get(r.name) == Severity.FAIL)

#TODO do we need property annotation here as well?
    def failed(self, severity_type: Severity) -> list[PortfolioLogRow]:
        sev = {s.name: s.severity for s in self.specs}  

        return [r for r in self.results if (not r.passed and sev.get(r.name) == severity_type)]

        

def run_raw_quality_checks(dataset: str, rows: list[PortfolioLogRow], specs: list[CheckSpec]) -> QualityReport:
    results: list[CheckResult] = []

    for s in specs:
        r = s.fn(rows)
        #TO THINK why do we change name? maybe better to fail here?
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



