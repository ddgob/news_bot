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

    def search(self, phrase: str) -> None:
        try:
            self.__logger('info', f'Searching phrase {phrase}...')
            search_button_locator: str = "//*[@data-element='search-button']"
            self.__handler.click_element_when_clickable(search_button_locator, timeout=30)
            search_input_field_locator: str = "//input[@data-element='search-form-input']"
            self.__handler.input_text_when_element_is_visible(search_input_field_locator, phrase)
            submit_button_locator: str = "//*[@data-element='search-submit-button']"
            self.__handler.click_element_when_clickable(submit_button_locator, timeout=30)
            self.__logger('info', f'Finished searching phrase {phrase}')
        except Exception as e:
            self.__logger('error', f'An error occurred while searching phrase {phrase}: {e}')

    def select_newest_articles(self) -> None:
        try:
            self.__logger('info', 'Selecting newest articles...')
            order_articles_dropdown_locator: str = "//select[@name='s']"
            self.__handler.wait_until_element_is_visible(order_articles_dropdown_locator, timeout=30)
            self.__handler.select_from_list_by_label(order_articles_dropdown_locator, 'Newest')
            # Wait for the newest articles to load
            articles_section_locator: str = 'class:search-results-module-results-menu'
            self.__logger('info', 'Finished selecting newest articles')
            self.__handler.wait_until_element_is_not_visible(articles_section_locator, timeout=1)
        except Exception as e:
            self.__logger('error', f'An error occurred while selecting the newest articles: {e}')