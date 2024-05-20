from RPA.Browser.Selenium import Selenium
from .logger import Logger

class LATimesBrowserHandler:

    __website_url: str = 'https://www.latimes.com/'

    def __init__(self, handler: Selenium, logger) -> None:
        self.__handler: Selenium = handler
        self.__logger = logger

    def open_website(self) -> None:
        try:
            self.__logger('info', f'Opening {self.__website_url} website...')
            self.__handler.open_available_browser('https://www.latimes.com/')
            self.__logger('info', f'Finished opening {self.__website_url} website')
        except Exception as e:
            self.__logger('error', f'An error occurred while opening the {self.__website_url} website: {e}')