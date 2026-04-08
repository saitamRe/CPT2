
from dataclasses import dataclass
import logging
import time
import random
from typing import Any, Callable, Type


@dataclass(frozen=True)
class RetryConfig:
    base_delay: float = 1.0
    max_attempts: int = 3
    jitter: float = 0.1
    backoff_factor: float = 1.0
    max_delay: float = 4.0
    retry_exceptions: tuple[Type[Exception], ...] = (Exception, )

    def __post_init__(self):
        if self.base_delay <= 0:
            raise ValueError('base_delay must be > 0')
        if self.max_attempts <= 0:
            raise ValueError('max_attempts must be > 0')
        if self.jitter < 0:
            raise ValueError('jitter must be >= 0')
        if self.backoff_factor < 1:
            raise ValueError('backoff_factor must be >= 1')
        if self.max_delay <= 0:
            raise ValueError('max_delay must be > 0')
        if not self.retry_exceptions:
            raise ValueError('retry_exceptions must not be empty')
        if not all(
            isinstance(exc, type) and issubclass(exc, Exception)
            for exc in self.retry_exceptions
        ):
            raise TypeError('retry_exceptions must contain only Exception classes')
    
def _calc_delay(config: RetryConfig, attempt: int) -> float:


    delay = config.base_delay * (config.backoff_factor ** (attempt - 1))

    if config.jitter > 0:
        delay += random.uniform(0, config.jitter)
    
    delay = min(delay, config.max_delay)
    
    return delay



def run_with_retry(
    input_func: Callable,
    step_name: str,
    logger: logging.Logger,
    config: RetryConfig,
    *args,
    **kwargs
) -> Any:

    for attempt in range(1, config.max_attempts + 1):     
        try:
            return input_func(*args, **kwargs)
        except config.retry_exceptions as exc:
            if attempt == config.max_attempts:
                logger.error(
                    f'{step_name} failed after {attempt} attempts'
                    f'with {type(exc).__name__}: {exc}',
                    exc_info=True
                )
                raise
            delay = _calc_delay(config, attempt)
            logger.warning(
                f'{attempt} attempt of {step_name} failed '
                f'with {type(exc).__name__}: {exc}'
                f'retry in {delay:.2f} sec'
            )
            time.sleep(delay)

    