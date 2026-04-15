import logging

from src.quality.policy import Severity
from src.quality.runner import QualityReport


def log_quality_report(
    logger: logging.Logger, 
    report: QualityReport, *, 
    step: str, 
    layer: str, 
    sample_limit: int = 5
    ):
    logger.info(
        "quality_check_finished",
        extra={
            'dataset': report.dataset,
            'run_id': report.run_id,
            'created_at': report.created_at,
            'passed': report.passed,
            'checks_total': len(report.results),
            'failed_with_fail_sev': len([1 for fr in report.failed(Severity.FAIL)]),
            'failed_with_warn_sev': len([1 for fr in report.failed(Severity.WARN)]),
        },
    )

    sev = {s.name: s.severity for s in report.specs}
     
    for r in report.results:

        trunc_samples = r.samples[:sample_limit]

        if r.passed:
            continue
        extended_log = logger.error if sev.get(r.name) == Severity.FAIL else logger.warning
        extended_log(
            'quality_check_failed', 
            extra={
                'dataset': report.dataset,
                'run_id': report.run_id,
                'severity': sev.get(r.name, Severity.LOG).value,
                'message': r.message,
                'stats': r.stats,
                'samples': trunc_samples,
            },
        )