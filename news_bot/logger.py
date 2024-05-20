import logging
from datetime import datetime, timedelta
import warnings

class Logger:
    
    _instance = None

    def __new__(cls, log_dir):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger(log_dir)
        return cls._instance
    
    def _initialize_logger(self, log_dir):
        self.logger = logging.getLogger('LATimesScraperLogger')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(f'{log_dir}/LATimesScraper_{datetime.now().strftime("%Y%m%d%H%M%S")}.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # Redirect warnings to the logger
        logging.captureWarnings(True)
        warn_handler = logging.StreamHandler()
        warn_handler.setLevel(logging.WARNING)
        warn_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        warn_handler.setFormatter(warn_formatter)
        self.logger.addHandler(warn_handler)

        def warn_with_logger(message, category, filename, lineno, file=None, line=None):
            self.logger.warning(warnings.formatwarning(message, category, filename, lineno, line))

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