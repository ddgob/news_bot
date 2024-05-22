from RPA.Browser.Selenium import Selenium
from .logger import Logger
from .articles.article_list import SearchArticleList
from .articles.article import Article, SearchArticle
from .date_handler import DateHandler
from datetime import datetime
from typing import Any
from .news_website_browser_handler import NewsWebsiteBrowserHandler

class LATimesBrowserHandler(NewsWebsiteBrowserHandler):
    __website_url: str = 'https://www.latimes.com/'

    def __init__(self, handler: Selenium) -> None:
        self.__handler: Selenium = handler
        self.__log = Logger().log

    def open_website(self) -> None:
        try:
            self.__log('info', f'Opening {self.__website_url} website...')
            self.__handler.open_available_browser(self.__website_url)
            self.__log(
                'info', f'Finished opening {self.__website_url} website'
            )
        except Exception as e:
            error_message: str = (
                f'An error occurred while opening the {self.__website_url} '
                f'website: {e}'
            )
            self.__log('error', error_message)

    def search(self, phrase: str) -> None:
        try:
            search_button_locator: str = "//*[@data-element='search-button']"
            search_input_field_locator: str = (
                "//input[@data-element='search-form-input']"
                )
            submit_button_locator: str = (
                "//*[@data-element='search-submit-button']"
                )
            self.__log('info', f'Searching phrase {phrase}...')
            self.__handler.click_element_when_clickable(
                search_button_locator, timeout=30
                )
            self.__handler.input_text_when_element_is_visible(
                search_input_field_locator, phrase
                )
            self.__handler.click_element_when_clickable(
                submit_button_locator, timeout=30
                )
            self.__log('info', f'Finished searching phrase {phrase}')
        except Exception as e:
            self.__log(
                'error', 
                f'An error occurred while searching phrase {phrase}: {e}'
            )

    def select_newest_articles(self) -> None:
        try:
            order_articles_dropdown_locator: str = "//select[@name='s']"
            articles_section_locator: str = (
                'class:search-results-module-results-menu'
                )
            self.__log('info', 'Selecting newest articles...')
            self.__handler.wait_until_element_is_visible(
                order_articles_dropdown_locator, timeout=30
                )
            self.__handler.select_from_list_by_label(
                order_articles_dropdown_locator, 'Newest'
                )
            # Wait for the newest articles to load
            self.__log('info', 'Finished selecting newest articles')
            self.__handler.wait_until_element_is_not_visible(
                articles_section_locator, timeout=1
                )
        except Exception as e:
            self.__log(
                'error', 
                f'An error occurred while selecting the newest articles: {e}'
            )

    def __get_article_web_elements(self, page_number: int) -> list[Any]:
        try:
            article_section_locator: str = (
                'class:search-results-module-results-menu'
                )
            self.__log(
                'info', f'Getting articles from page {page_number}...'
                )
            self.__handler.wait_until_element_is_visible(
                article_section_locator, timeout=30
                )
            article_section_web_element: Any = self.__handler.find_element(
                article_section_locator
                )
            article_locator: str = 'tag:li'
            article_web_elements: Any = self.__handler.find_elements(
                article_locator, parent=article_section_web_element
                )
            self.__log(
                'info', 
                f'Finished getting articles from page {page_number}'
            )
            return article_web_elements
        except Exception as e:
            error_message: str = (
                f'An error occurred when getting the web elements for the '
                f'articles on page {page_number}: {e}'
            )
            self.__log('error', error_message)
            raise
        
    def __get_article(
            self, article_web_element: Any, article_number: int, 
            page_number: int) -> Article:
        try:
            # Define locators
            title_locator: str = 'class:promo-title'
            description_locator: str = 'class:promo-description'
            date_locator: str = 'class:promo-timestamp'
            image_locator: str = 'class:image'
            # Get values
            title: str = self.__handler.find_element(
                title_locator, parent=article_web_element
                ).text
            description: str = self.__handler.find_element(
                description_locator, parent=article_web_element
                ).text
            unconverted_date: str = self.__handler.find_element(
                date_locator, parent=article_web_element
                ).text
            image_src: str = self.__handler.find_element(
                image_locator, parent=article_web_element
                ).get_attribute('src')
            # Convert values
            date_handler: DateHandler = DateHandler()
            date: datetime = date_handler.convert_date_to_datetime(
                unconverted_date
                )
            # Create article
            article = Article(title, date, description, image_src)
            return article
        except Exception as e:
            error_message: str = (
                f'An error occurred while getting values for article '
                f'{article_number} in page {page_number}: {e}'
            )
            self.__log('error', error_message)
            raise

    def get_articles(self, search_phrase: str, 
                     page_number: int) -> SearchArticleList:
        try:
            search_articles: SearchArticleList = SearchArticleList(
                search_phrase
                )
            article_web_elements: Any = self.__get_article_web_elements(
                page_number
                )
            for article_number, article_web_element in enumerate(
                article_web_elements, start=1
                ):
                article: Article = self.__get_article(
                    article_web_element, article_number, page_number
                    )
                search_article: SearchArticle = SearchArticle.from_article(
                    article, search_phrase
                    )
                search_articles.append(search_article)
            return search_articles
        except Exception as e:
            error_message: str = (
                f'An error occurred while getting values for articles in page '
                f'{page_number}: {e}'
            )
            self.__log('error', error_message)
            raise
    
    def move_to_next_article_page(self, current_page_number: int) -> bool:
        try:
            next_page_button_parent_locator: str = (
                'class:search-results-module-next-page'
            )
            self.__handler.wait_until_element_is_visible(
                next_page_button_parent_locator, timeout=30
                )
            next_page_button_parent: Any = self.__handler.find_element(
                next_page_button_parent_locator
                )
            next_page_button_locator: str = 'tag:a'
            next_page_button: Any = self.__handler.find_element(
                next_page_button_locator, parent=next_page_button_parent
                )
            self.__handler.click_element_when_clickable(
                next_page_button, timeout=30
                )
            return True
        except Exception as e:
            if current_page_number == 10:
                warning_message: str = (
                    f'Could not move to next page {current_page_number + 1} '
                    f'due to search results only return 10 pages of results.'
                )
                self.__log('warning', warning_message)
                return False
            error_message: str = (
                f'An error occurred while moving from page '
                f'{current_page_number} to page {current_page_number + 1} '
                f'next page: {e}'
            )
            self.__log('error', error_message)
            raise

    def close_browser(self) -> None:
        try:
            self.__log('info', 'Closing browser...')
            self.__handler.close_browser()
            self.__log('info', 'Finished closing browser')
        except Exception as e:
            error_message: str = (
                f'An error occurred while closing the browser: {e}'
            )
            self.__log('error', error_message)
            raise

