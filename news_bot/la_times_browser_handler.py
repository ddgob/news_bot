from RPA.Browser.Selenium import Selenium
from .logger import Logger

class LATimesBrowserHandler:

    __website_url = 'https://www.latimes.com/'

    def __init__(self, log_dir):
        self.__la_times_browser_handler = Selenium()
        self.__logger = Logger(log_dir).log

    def open_website(self):
        try:
            self.__logger('info', f'Opening {self.__website_url} website...')
            self.__la_times_browser_handler.open_available_browser('https://www.latimes.com/')
            self.__logger('info', f'Finished opening {self.__website_url} website')
        except Exception as e:
            self.logger('error', f'An error occurred while opening the {self.__website_url} website: {e}')