"""Make Logger instance.

Author:
    Kibum Park
E-mail:
    castedice1@gmail.com
"""

import inspect
import json
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from types import TracebackType
from typing import Any

HOST = os.uname().nodename
LOG_DIR_PATH = Path("./logs")
LOG_DIR_PATH.mkdir(exist_ok=True, parents=True)
LOG_PATH = LOG_DIR_PATH / f"{HOST}.log"
TRACE = 15
CONSOLE_LOG_FORMAT = (
    f"[{HOST}][%(asctime)s] %(levelname)-8s >> "
    + "%(filename)s : %(lineno)4s - %(message)s"
)
CONSOLE_LOG_FORMAT_FOR_DECORATOR = (
    f"[{HOST}][%(asctime)s] %(levelname)-8s >> %(message)s"
)
JSON_FORMAT_KEYS = {
    "level": "levelname",
    "message": "message",
    "loggerName": "name",
    "processName": "processName",
    "processID": "process",
    "threadName": "threadName",
    "threadID": "thread",
    "timestamp": "asctime",
    "lineNo": "lineno",
    "functionName": "funcName",
}


class TraceLogLevel(logging.Logger):
    """New log level for trace process."""

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)


class ConsoleFormatter(logging.Formatter):
    """Format logs for console."""

    blue = "\x1b[34;20m"
    green = "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    formats = {
        logging.DEBUG: blue + CONSOLE_LOG_FORMAT + reset,
        TRACE: green + CONSOLE_LOG_FORMAT + reset,
        logging.INFO: grey + CONSOLE_LOG_FORMAT + reset,
        logging.WARNING: yellow + CONSOLE_LOG_FORMAT + reset,
        logging.ERROR: red + CONSOLE_LOG_FORMAT + reset,
        logging.CRITICAL: bold_red + CONSOLE_LOG_FORMAT + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Make format for console.

        Override `logging.LogRecord`

        Args:
            record (logging.LogRecord) : `logging.LogRecord` module.

        Returns:
            str : Formatted logs.

        # noqa: DAR101 arg1
        """
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class ConsoleFormatterDecorator(logging.Formatter):
    """Format logs for console."""

    blue = "\x1b[34;20m"
    green = "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    formats = {
        logging.DEBUG: blue + CONSOLE_LOG_FORMAT_FOR_DECORATOR + reset,
        TRACE: green + CONSOLE_LOG_FORMAT_FOR_DECORATOR + reset,
        logging.INFO: grey + CONSOLE_LOG_FORMAT_FOR_DECORATOR + reset,
        logging.WARNING: yellow + CONSOLE_LOG_FORMAT_FOR_DECORATOR + reset,
        logging.ERROR: red + CONSOLE_LOG_FORMAT_FOR_DECORATOR + reset,
        logging.CRITICAL: bold_red + CONSOLE_LOG_FORMAT_FOR_DECORATOR + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Make format for console.

        Override `logging.LogRecord`

        Args:
            record (logging.LogRecord) : `logging.LogRecord` module.

        Returns:
            str : Formatted logs.

        # noqa: DAR101 arg1
        """
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class JsonFormatter(logging.Formatter):
    """Format logs for ELK stack.

    Args:
        fmt_dict (dict): logging format attribute pairs. Defaults to {"message": "message"}.
        time_format (str): time.strftime() format string. Defaults to ISO format "%Y-%m-%dT%H:%M:%S"
        msec_format (str): Microsecond formatting. Appended at the end. Default: "%s.%03dZ"
    """

    def __init__(
        self,
        fmt_dict: dict | None = None,
        time_format: str = "%Y-%m-%dT%H:%M:%S",
        msec_format: str = "%s.%06d",
    ) -> None:
        self.fmt_dict = (
            fmt_dict if fmt_dict is not None else {"message": "message"}
        )
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        """Overwritten to look for the attribute in the format dict values instead of the fmt string."""
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record) -> dict:
        """Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string.
        KeyError is raised if an unknown attribute is provided in the fmt_dict.
        """
        return {
            fmt_key: record.__dict__[fmt_val]
            for fmt_key, fmt_val in self.fmt_dict.items()
        }

    def format(self, record) -> str:
        """Mostly the same as the parent's class method, the difference being that a dict is manipulated and dumped as JSON instead of a string."""
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(message_dict, default=str)


def make_logger(name) -> logging.Logger:
    """Make logger instance.

    Format is`[YYYY-MM-DD hh:mm:ss,ms] <LEVEL>  >> <FILENAME> : <LINENO> - <MESSAGE>`

    Args:
        name (str, optional): Set `__name__` when calling logger.

    Returns:
        logging.Logger: Logging instance.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.handlers.clear()
    logging.setLoggerClass(TraceLogLevel)
    logging.addLevelName(TRACE, "TRACE")
    if name == "":
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console_formatter = ConsoleFormatter()
    console.setFormatter(console_formatter)
    logger.addHandler(console)

    file_handler = TimedRotatingFileHandler(
        filename=LOG_PATH, when="W0", backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = JsonFormatter(JSON_FORMAT_KEYS)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def make_logger_for_decorator(name, cache=None) -> logging.Logger:
    """Make logger instance.

    Format is`[YYYY-MM-DD hh:mm:ss,ms] <LEVEL>  >> <FILENAME> : <LINENO> - <MESSAGE>`

    Args:
        name (str, optional): Set `__name__` when calling logger.

    Returns:
        logging.Logger: Logging instance.
    """
    if cache is None:
        cache = {}
    if (name not in cache) or (name == ""):
        cache[name] = make_logger(name)

    return cache[name]


def hook_exception(
    exc_type: Any,
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> None:
    """Catch exception when unexpected exceptions occur.

    Args:
        exc_type (Any): Exception type.
        exc_value (BaseException): Exception value.
        exc_traceback (TracebackType, optional): Traceback.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    logger.critical(
        "Unexpected exception", exc_info=(exc_type, exc_value, exc_traceback)
    )


def log(func):
    """Logging Decorator."""

    def wrapper(*args, **kwargs):
        logger = make_logger_for_decorator(__name__)
        _lines, line_num = inspect.getsourcelines(func)
        logger.info(
            f"{func.__module__} : {line_num:4} -  {func.__name__} started."
        )
        result = func(*args, **kwargs)
        logger.info(
            f"{func.__module__} : {line_num:4} - {func.__name__} ended."
        )

        return result

    return wrapper


def debug(func):
    """Debug Logging Decorator."""

    def wrapper(*args, **kwargs):
        logger = make_logger_for_decorator(__name__)
        _lines, line_num = inspect.getsourcelines(func)

        arg_pairs = [
            (f"arg{i}", type(arg).__name__, arg)
            for i, arg in enumerate(args, 1)
        ]
        kwargs_pairs = [
            (key, type(value).__name__, value) for key, value in kwargs.items()
        ]

        logger.debug(
            f"{func.__module__} : {line_num:4} - {func.__name__} with arguments: args={arg_pairs}, kwargs={kwargs_pairs}"
        )

        result = func(*args, **kwargs)

        logger.debug(
            f"{func.__module__} : {line_num:4} - {func.__name__} returned ({type(result).__name__}) {result}"
        )

        return result

    return wrapper


def trace(func):
    """Trace Logging Decorator."""

    def wrapper(*args, **kwargs):
        logger = make_logger_for_decorator(__name__)
        _lines, line_num = inspect.getsourcelines(func)
        result = func(*args, **kwargs)
        logger.trace(
            f"{func.__module__} : {line_num:4} - {func.__name__} is Done."
        )
        return result

    return wrapper


logger = make_logger("")
sys.excepthook = hook_exception
