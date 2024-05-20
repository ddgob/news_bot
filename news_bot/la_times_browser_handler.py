from RPA.Browser.Selenium import Selenium
from .logger import Logger

class LATimesBrowserHandler:

    __website_url = 'https://www.latimes.com/'

    def __init__(self, log_dir):
        self.__la_times_browser_handler = Selenium()
        self.__logger = Logger(log_dir).log