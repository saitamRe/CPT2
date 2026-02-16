from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any

from src.dto.portfolio_dto import PortfolioLogRow

@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    samples: list[dict[str, Any]] = field(default_factory=list)
    stats: dict[str, int]  = field(default_factory=dict)
    message: str = ''

def _preview_row(row: PortfolioLogRow) -> dict[str, Any]:
    return {
        'timestamp': row.timestamp.isoformat() if isinstance(row.timestamp, datetime) else repr(row.timestamp),
        'symbol': row.symbol,
        'price': str(row.price),
        'quantity': str(row.quantity),
        'amount': str(row.amount),
    }

def check_symbol_str_and_non_empty(rows: list[PortfolioLogRow], sample_size: int = 20):
    total = 0
    bad = 0
    samples: list[dict[str, Any]] = []

    for row in rows:
        total += 1

        if not isinstance(row.symbol, str) or row.symbol.strip() == '':
            bad += 1
            if len(samples) <= sample_size:
                    samples.append({'reason': 'not_string', 'row': _preview_row(row)})

    passed = bad == 0

    return CheckResult(
        name='symbol_str_and_non_empty',
        passed=passed,
        samples=samples,
        stats={'rows_total': total, 'bad_symbol': bad},
        message='' if passed else f'{bad} rows have empty/non-string symbols'
    )


def check_decimal_finite_non_negative(rows: list[PortfolioLogRow], sample_size: int = 20) -> CheckResult:
    total = 0
    bad = 0
    negative = 0
    non_finite = 0
    samples: list[dict[str, Any]] = []

    

    def _check_decimal(name: str, d: Any ):
        issues = []
        if not isinstance(d, Decimal):
            issues.append({'name': name, 'reason': 'non_decimal', 'value': repr(d)})
            return issues
        if not d.is_finite():
            issues.append({'name': name, 'reason': 'non_finite', 'value': str(d)})
        if d < 0:
            issues.append({'name': name, 'reason': 'negative', 'value': str(d)})
        return issues

    for row in rows:
        total += 1
        issues = []
        issues += _check_decimal('price', row.price)
        issues += _check_decimal('quantity', row.quantity)
        issues += _check_decimal('amount', row.amount)

        for issue in issues:
            bad += 1
            if issue['reason'] == 'non_finite':
                non_finite += 1
            if issue['reason'] == 'negative':
                negative += 1

        if len(samples) < sample_size:
            samples.append({'issues': issues, 'row': _preview_row(row)})
            
    passed = bad == 0

    return CheckResult(
        name='decimal_finite_non_negative',
        passed=passed,
        samples=samples,
        stats={
            'rows_total': total,
            'bad': bad,
            'negative': negative,
            'non_finite': non_finite,
        },
        message='' if passed else f'{bad} rows have invalid decimal values'
    )


def check_timestamp_utc_or_naive(rows: list[PortfolioLogRow], sample_size: int = 20) -> CheckResult:
        total = 0
        bad = 0
        samples: list[dict[str, Any]] = []

        for row in rows:
            total += 1
            ts = row.timestamp
            if not isinstance(ts, datetime):
                bad += 1

                if len(samples) < sample_size:
                    samples.append({'reason': 'not_datetime', 'row': _preview_row(row)})
                
                continue

            #TODO warn policy for non-utc ts
            #if ts.tzinfo is not None:
        
        passed = bad == 0

        return CheckResult(
            name = 'timestamp_utc_or_naive',
            passed=passed,
            samples=samples,
            stats={
                'rows_total': total,
                'bad': bad,
            },
            message='' if passed else f'{bad} rows have invalid timestamps',
        )



                

    
            