import logging
import os
import sys
from typing import ClassVar, Optional
from dataclasses import dataclass, field
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init as colorama_init

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
    name: str = "logger"
    log_dir: str = "logs"
    max_bytes: int = 5 * 1024 * 1024
    capture_external: bool = True

    logger: logging.Logger = field(init=False)
    log_file: str = field(init=False)
    
    _instance: ClassVar[Optional["Logger"]] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __post_init__(self):
        if Logger._initialized:
            print('initialized 66666666666666')
            return
        Logger._initialized = True
        print('logger initialized xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        self.log_file = os.path.join(self.log_dir, f"{self.name}.log")
        os.makedirs(self.log_dir, exist_ok=True)

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        self._configure_handlers()

        if self.capture_external:
            self._capture_external_loggers()

    def _configure_handlers(self):
        log_format = (
            "%(asctime)s | %(levelname)-8s | %(name)s | "
            "%(filename)s:%(lineno)d | %(message)s"
        )
        date_format = "%Y-%m-%d %H:%M:%S"

        # Console handler with colors
        color_formatter = _ColorFormatter(log_format, date_format)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(color_formatter)
        self.logger.addHandler(stream_handler)

        # File handler with rotation
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler = RotatingFileHandler(
            self.log_file, maxBytes=self.max_bytes, backupCount=0, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def _capture_external_loggers(self):
        return
        for ext_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "dash"):
            ext_logger = logging.getLogger(ext_name)
            # for handler in self.logger.handlers:
            #     if handler not in ext_logger.handlers:
            #         print('added handler', handler.get_name)
            #         ext_logger.addHandler(handler)
            # ext_logger.setLevel(level)
            ext_logger.propagate = True

    @property
    def get_logger(self) -> logging.Logger:
        print('fetched zzzzzzzzzzzzzzzzzz')
        return self.logger
