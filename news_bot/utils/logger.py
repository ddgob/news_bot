import logging
from datetime import datetime, timedelta
import warnings
from .. import config

class Logger:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)
            cls.__instance._initialize_logger()
        return cls.__instance
    
    def _initialize_logger(self):
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

        def warn_with_logger(message, category, filename, lineno, file=None, 
                             line=None):
            self.logger.warning(warnings.formatwarning(message, category, 
                                                       filename, lineno, line))

        warnings.showwarning = warn_with_logger

    def log(self, level, message):
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