import logging
import os
import sys
from typing import ClassVar, Optional
from dataclasses import dataclass, field
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init as colorama_init

from deploy_chatbot_python.config import constants

colorama_init(autoreset=True)


class _ColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Style.DIM,
        logging.INFO: Style.NORMAL,
        logging.WARNING: Fore.YELLOW + Style.BRIGHT,
        logging.ERROR: Fore.RED + Style.BRIGHT,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + Style.BRIGHT,
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, Style.NORMAL)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


@dataclass
class Logger:
    name: str
    level: str = constants.LOGGER_LEVEL
    max_bytes: int = constants.LOG_FILE_MAX_BYTES
    capture_external: bool = True

    logger: logging.Logger = field(init=False)

    _instance: ClassVar[Optional["Logger"]] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls, *args, **kwargs):  # pylint: disable=unused-argument
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __post_init__(self):
        if Logger._initialized:
            return
        Logger._initialized = True
        os.makedirs(constants.LOG_DIR_PATH, exist_ok=True)

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.logger.propagate = False

        self._configure_handlers()

        if self.capture_external:
            self._capture_external_loggers()

    def _configure_handlers(self):
        log_format = (
            "%(asctime)s | %(levelname)-s | %(name)s | "
            "%(filename)s:%(lineno)d | %(message)s"
        )
        date_format = "%Y-%m-%d %H:%M:%S"

        # Console handler with colors
        color_formatter = _ColorFormatter(log_format, date_format)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(color_formatter)
        self.logger.addHandler(stream_handler)

        # File handler with rotation
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler = RotatingFileHandler(
            constants.LOG_FILE_PATH, maxBytes=self.max_bytes, backupCount=0, encoding="utf-8"
        )
        file_handler.setLevel(self.level)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def _capture_external_loggers(self):
        all_external_loggers_names = logging.Logger.manager.loggerDict.keys()
        for ext_logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "dash"):
            if ext_logger_name not in all_external_loggers_names:
                continue
            ext_logger = logging.getLogger(ext_logger_name)
            ext_logger.propagate = True

    @property
    def get_logger(self) -> logging.Logger:
        return self.logger
