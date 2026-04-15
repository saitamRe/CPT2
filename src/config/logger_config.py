import json
import logging
import os
import sys
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from typing import Any

_run_id: ContextVar[str] = ContextVar('run_id', default='-')
_step: ContextVar[str] = ContextVar('step', default='-')
_pipeline: ContextVar[str] = ContextVar('pipeline', default='cpt')

def set_run_id(run_id: str) -> None:
    _run_id.set(run_id)

def set_step(step: str) -> None:
    _step.set(step)

def set_pipeline(pipeline: str) -> None:
    _pipeline.set(pipeline)

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base: dict[str, Any] = {
            'ts': datetime.fromtimestamp(
                record.created, 
                tz=timezone.utc).isoformat(timespec='milliseconds'),
            'level': record.levelname,
            'logger': record.name,
            'msg': record.getMessage(),
            'run_id': _run_id.get(),
            'pipeline': _pipeline.get(),
            'step': _step.get()
        }

        for k, v in record.__dict__.items():
            if k.startswith('_'):
                continue
            if k in("args", "msg", "levelname", "levelno", "name", "created", "msecs",
                     "relativeCreated", "pathname", "filename", "module", "exc_info",
                     "exc_text", "stack_info", "lineno", "funcName", "thread", "threadName",
                     "processName", "process"):
                continue

            if k not in base:
                base[k] = v
            
        if record.exc_info:
            base['exc'] = self.formatException(record.exc_info)
            
        return json.dumps(base, ensure_ascii=False) + '\n'

def setup_logging(*, level: str | None = None, log_file: str | None = None) -> None:
    logger = logging.getLogger()
    logger.handlers.clear()

    lvl = (level or os.getenv('LOG_LEVEL', 'INFO')).upper()
    logger.setLevel(lvl)

    fmt = JsonFormatter()
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    if log_file:
        #to switch to another file when we reached 5mb
        fh = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

def get_new_run_id() -> str:
        return uuid.uuid4().hex


