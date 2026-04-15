
from src.utils.retry import RetryConfig


def test_retry_config_default_values():
    config = RetryConfig()

    assert config.base_delay == 1.0
    assert config.max_attempts == 3
    assert config.jitter == 0.1
    assert config.backoff_factor == 1.0
    assert config.max_delay == 4.0
    assert config.retry_exceptions == (Exception, ...)


