"""
This module provides a singleton Logger class for logging messages in the news bot application.

The Logger class sets up a logger that writes logs to a file and captures warnings.
It ensures that only one instance of the logger is created and provides methods for logging
messages at various levels (debug, info, warning, error, critical).
"""

import logging
from datetime import datetime
import warnings

from news_bot import config

class Logger:
    """
    Singleton class for logging messages in the news bot application.
    
    This class sets up a logger that writes logs to a file and captures 
    warnings.
    """

    __instance = None

    def __new__(cls):
        """
        Create a new instance of Logger if it does not already exist.

        Returns:
            Logger: The singleton instance of the Logger class.
        """
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)
            cls.__instance._initialize_logger()
        return cls.__instance

    def __init__(self):
        """
        Initialize the logger attribute if it has not been initialized yet.
        """
        if not hasattr(self, 'logger'):
            self.logger = None

    def _initialize_logger(self):
        """
        Initialize the logger instance.

        Sets up the file handler, formatter, and warning capture.
        """
        self.logger = logging.getLogger('news_bot_logger')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            f'{config.LOG_FILE_DIR}/news_bot_logger_'
            f'{datetime.now().strftime("%m-%d-%Y_%H:%M:%S")}.log'
        )
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # Redirect warnings to the logger
        logging.captureWarnings(True)
        warn_handler = logging.StreamHandler()
        warn_handler.setLevel(logging.WARNING)
        warn_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        warn_handler.setFormatter(warn_formatter)
        self.logger.addHandler(warn_handler)

        def warn_with_logger(message, category, filename, lineno, line=None):
            """
            Log warnings with the logger.

            Args:
                message: The warning message.
                category: The category of the warning.
                lineno: The line number where the warning occurred.
                file: The file object (default: None).
                line: The line of code where the warning occurred 
                (default: None).
            """
            self.logger.warning(warnings.formatwarning(message, category,
                                                       filename, lineno, line))

        warnings.showwarning = warn_with_logger

    def log(self, level, message):
        """
        Log a message at the specified log level.

        Args:
            level (str): The log level ('debug', 'info', 'warning', 
            'error', 'critical').
            message (str): The message to log.

        Raises:
            ValueError: If the log level is not recognized.
        """
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)
