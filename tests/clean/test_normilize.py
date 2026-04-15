from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pytest

from src.cleaning.cleaner import (
    _ensure_decimal,
    _ensure_ts,
    _norm_symbol,
    iter_clean_portfolio_snapshot,
)
from src.dto.portfolio_dto import PortfolioLogRow


@pytest.mark.parametrize('input, expected', 
[
    (
        datetime(2026, 1, 1, 12, 0, 0),
        datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    ),
    (
        datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    ),
    (
        datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone(timedelta(hours=3))),
        datetime(2026, 1, 1, 9, 0, 0, tzinfo=timezone.utc)
    )
])
def test_ensure_ts_valid(input, expected):
    assert _ensure_ts(input) == expected

@pytest.mark.parametrize('input', [
    None,
    2026,
    '2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc',
    '0',
    0,
    -1,
    1704100800,
    1704100800.0,
    date(2024, 1, 1)
])
def test_ensure_ts_invalid(input):
    with pytest.raises(TypeError):
        _ensure_ts(input)

@pytest.mark.parametrize('input, expected', 
    [
        ("btc", "BTC"),
        (" BTC ", "BTC"),
        ("eth_usdt", "ETH_USDT"),
        ("apt-coin", "APT-COIN"),
        ("ABC123", "ABC123"),
        ("a_b-c9", "A_B-C9"),
    ],
)
def test_norm_symbol_valid(input, expected):
    assert _norm_symbol(input) == expected

@pytest.mark.parametrize('input',
[
        None,
        123,
        12.5,
        ["BTC"],
        {"sym": "BTC"},
    ]
)
def test_norm_symbol_negative_invalid_type_error(input):
    with pytest.raises(TypeError):
        _norm_symbol(input)

@pytest.mark.parametrize(
    "bad_sym",
    [
        "",          # empty
        "   ",       # whitespace only
        "\n\t",      # whitespace
        "btc/usdt",  # slash
        "eth.usdt",  # dot
        "btc usdt",  # space inside
        "btc@usdt",  # special char
        "äbc",       # non-ascii
        "₿TC",       # unicode symbol
        " btc/usdt ",# looks ok before strip
    ],
)
def test_norm_symbol_invalid_value_error(bad_sym):
    with pytest.raises(ValueError):
        _norm_symbol(bad_sym)


@pytest.mark.parametrize(
    "value",
    [
        Decimal("0"),
        Decimal("1"),
        Decimal("1.23"),
        Decimal("1000000000.00000001"),
    ],
)
def test_ensure_decimal_valid(value):
    result = _ensure_decimal(value, "price")
    assert result is value


@pytest.mark.parametrize(
    "bad_value",
    [
        1.23,          # float (explicitly forbidden)
        1,             # int
        "1.23",        # str
        None,
        True,
    ],
)
def test_ensure_decimal_invalid_type_error(bad_value):
    with pytest.raises(TypeError):
        _ensure_decimal(bad_value, "amount")


@pytest.mark.parametrize(
    "bad_decimal",
    [
        Decimal("NaN"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
        Decimal("-0.01"),
    ],
)
def test_ensure_decimal_invalid_value_error(bad_decimal):
    with pytest.raises(ValueError):
        _ensure_decimal(bad_decimal, "quantity")

def test_iter_clean_portfolio_snapshot_positive():
    rows = [
        PortfolioLogRow(
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
            symbol=' bTc ',
            price=Decimal('2'),
            quantity=Decimal('2'),
            amount=Decimal('4')
        ),
        PortfolioLogRow(
            timestamp=datetime(2026, 2, 1, 11, 0, 0, tzinfo=timezone(timedelta(hours=3))),
            symbol=' eth_USdt ',
            price=Decimal('3'),
            quantity=Decimal('3'),
            amount=Decimal('9')
        ),
    ]

    out = list((iter_clean_portfolio_snapshot(iter(rows))))

    assert len(out) == 2

    assert out[0].timestamp == datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert out[0].symbol == 'BTC'
    assert out[0].price == Decimal('2')
    assert out[0].quantity == Decimal('2')
    assert out[0].amount == Decimal('4')

    assert out[1].timestamp == datetime(2026, 2, 1, 8, 0, 0, tzinfo=timezone.utc)
    assert out[1].symbol == 'ETH_USDT'

def test_iter_clean_portfolio_snapshot_negative():
    rows = [
        PortfolioLogRow(
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
            symbol=' bTc ',
            price=Decimal('2'),
            quantity=Decimal('2'),
            amount=Decimal('4')
        ),
        PortfolioLogRow(
            timestamp=datetime(2026, 2, 1, 11, 0, 0, tzinfo=timezone(timedelta(hours=3))),
            symbol=' eth_USdt ',
            price=3.1,
            quantity=Decimal('3'),
            amount=Decimal('9')
        ),
    ]

    gen = iter_clean_portfolio_snapshot(iter(rows))

    first = next(gen)
    assert first.symbol == "BTC"

    with pytest.raises(TypeError):
        next(gen)

def exploading_gen():
    yield PortfolioLogRow(
        timestamp=datetime(2026, 1, 1, 12, 0, 0),
            symbol=' bTc ',
            price=Decimal('2'),
            quantity=Decimal('2'),
            amount=Decimal('4')
    )

    raise RuntimeError("should not be touched yet")

def test_iter_clean_portfolio_snapshot_laziness():
     gen = iter_clean_portfolio_snapshot(exploading_gen())
     with pytest.raises(RuntimeError):
        next(gen)

    



