import logging
import os
import sys
from functools import wraps

from ansi import Ansi


class AnsiLogFormatter(logging.Formatter):
    LOG_STRING_FMT = "%(name)s:(%(filename)s:%(lineno)d) - %(message)s"

    def __init__(self, use_color: bool | None = None):
        super().__init__()
        self.use_color = self._detect_color_support() if use_color is None else use_color

        if not self.use_color:
            Ansi.disable()

        self.FORMATS = {
            logging.DEBUG: Ansi.fmt_prefix([Ansi.BLUE], "DEBUG", self.LOG_STRING_FMT),
            logging.INFO: Ansi.fmt_prefix([Ansi.GREEN], "INFO", self.LOG_STRING_FMT, padding='  '),
            logging.WARNING: Ansi.fmt_prefix([Ansi.YELLOW], "WARN", self.LOG_STRING_FMT, padding='  '),
            logging.ERROR: Ansi.fmt_prefix([Ansi.RED], "ERROR", self.LOG_STRING_FMT),
            logging.CRITICAL: Ansi.fmt_prefix([Ansi.RED, Ansi.BOLD], "CRITICAL", self.LOG_STRING_FMT),
        }

    @staticmethod
    def _detect_color_support() -> bool:
        if os.getenv("NO_COLOR") is not None:
            return False

        if not sys.stdout.isatty() and not sys.stderr.isatty():
            return False

        term = os.getenv("TERM", "")
        if term == "dumb":
            return False

        return True

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.LOG_STRING_FMT)
        fmt = logging.Formatter(log_fmt)
        return fmt.format(record)


def logger_init(span: str | None = None, level=logging.DEBUG, use_color: bool | None = None) -> logging.Logger:
    logger = logging.getLogger(span)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(AnsiLogFormatter(use_color))
    logger.addHandler(handler)

    return logger


def with_logger(name: str | None = None):
    """Decorator that injects a logger into the function scope as 'log'."""
    def decorator(func):
        log = logger_init(name)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs, log=log)
        return wrapper
    return decorator