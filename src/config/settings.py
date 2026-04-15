import json
import os
from dataclasses import dataclass

from src.utils.retry import RetryConfig

#possible future: split config on api, db and etc

def require_var(var_name: str):
    env_var = os.getenv(var_name)
    if not env_var:
        raise ValueError(f'{var_name} is required but not set')
    return env_var

def require_var_int(var_name: str) -> int:
    env_var = os.getenv(var_name)

    if not env_var:
        raise ValueError(f'{var_name} is required but not set')
    
    try:
        return int(env_var)
    except ValueError:
        raise ValueError(f'{var_name} must be integer, got {env_var}')
    

def require_json(var_name: str) -> dict:
    val = require_var('PORTFOLIO')
    try:
        return json.loads(require_var('PORTFOLIO'))
    except json.JSONDecodeError:
        raise ValueError(f'{var_name} must be valid JSON, got {val}')

@dataclass(frozen=True)
class Settings:
    request_timeout: int
    binance_api_base: str
    price_url: str
    db_dsn: str
    portfolio: dict[str, float]
    clean_batch_size: int
    binance_retry_config: RetryConfig

    @classmethod
    def init_config_from(cls) -> 'Settings':
        request_timeout = require_var_int("REQUEST_TIMEOUT")
        binance_api_base = require_var("BINANCE_API_BASE")
        price_url = require_var("PRICE_URL")
        db_dsn = require_var("DB_DSN")
        portfolio = require_json("PORTFOLIO")
        clean_batch_size = require_var_int("CLEAN_BATCH_SIZE")

        if request_timeout <= 0:
                raise ValueError("REQUEST_TIMEOUT must be > 0")

        if clean_batch_size <= 0:
            raise ValueError("CLEAN_BATCH_SIZE must be > 0")

        if not binance_api_base.startswith("http"):
            raise ValueError("BINANCE_API_BASE must start with http")

        if not price_url.startswith("/"):
            raise ValueError("PRICE_URL must start with /")

        if not isinstance(portfolio, dict):
            raise ValueError("PORTFOLIO must be a JSON object")

        if not portfolio:
            raise ValueError("PORTFOLIO must not be empty")

        for asset, qty in portfolio.items():
            if not isinstance(asset, str) or not asset.strip():
                raise ValueError(f"PORTFOLIO contains invalid asset key: {asset}")

            if not isinstance(qty, (int, float)):
                raise ValueError(
                    f"PORTFOLIO value for {asset} must be int or float, got {type(qty).__name__}"
                )

            if qty < 0:
                raise ValueError(f"PORTFOLIO value for {asset} must be >= 0")

        if not db_dsn:
            raise ValueError('DB_DSN cant be empty')
        
        if not isinstance(db_dsn, str):
            raise ValueError(f'DB_DSN must be str type, got {type(db_dsn).__name__}')
        
        return cls(
            request_timeout=request_timeout,
            binance_api_base=binance_api_base,
            price_url=price_url,
            db_dsn=db_dsn,
            portfolio=portfolio,
            clean_batch_size=clean_batch_size,
            binance_retry_config=RetryConfig(
                max_attempts=3,
                base_delay=0.5,
                max_delay=5,
                backoff_factor=2,
                jitter=0.1,
                retry_exceptions=(TimeoutError, ConnectionError),
            ),
        )
        

settings = Settings.init_config_from()



