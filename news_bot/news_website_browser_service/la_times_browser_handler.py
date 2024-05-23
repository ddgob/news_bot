"""
This module defines the LATimesBrowserHandler class, which is a concrete 
implementation of the NewsWebsiteBrowserHandler abstract base class. It is 
used for handling browser interactions with the LA Times website using 
Selenium. The class includes methods for opening the website, performing 
searches, selecting the newest articles, getting article details, moving to 
the next page of articles, and closing the browser.

Classes:
    LATimesBrowserHandler: A browser handler for scraping articles from 
    the LA Times website.
"""

from datetime import datetime
from typing import Any

from RPA.Browser.Selenium import Selenium

from ..utils import Logger
from ..articles.article_list import SearchArticleList
from ..articles.article import Article, SearchArticle
from ..utils import DateHandler
from .news_website_browser_handler import NewsWebsiteBrowserHandler


class LATimesBrowserHandler(NewsWebsiteBrowserHandler):
    """
    Browser handler for scraping articles from the LA Times website.
    """

    __website_url: str = 'https://www.latimes.com/'

    def __init__(self, handler: Selenium) -> None:
        """
        Initialize the LATimesBrowserHandler.

        Args:
            handler (Selenium): The Selenium browser handler.
        """
        self.__handler: Selenium = handler
        self.__log = Logger().log

    def open_website(self) -> None:
        """
        Open the LA Times website in a browser.

        Returns:
            None

        Raises:
            Exception: If an error occurs while opening the website.
        """
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
        """
        Search for articles on the LA Times website using the specified 
        phrase.

        Args:
            phrase (str): The search phrase to use.

        Returns:
            None

        Raises:
            Exception: If an error occurs while performing the search.
        """
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
            if 'not visible after' in str(e):
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
                return
            self.__log(
                'error', 
                f'An error occurred while searching phrase {phrase}: {e}'
            )

    def select_newest_articles(self) -> None:
        """
        Select the newest articles on the LA Times website.

        Returns:
            None

        Raises:
            Exception: If an error occurs while selecting the newest 
            articles.
        """
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
            if 'still visible after' in str(e):
                return
            self.__log(
                'error', 
                f'An error occurred while selecting the newest articles: {e}'
            )

    def __get_article_web_elements(self, page_number: int) -> list[Any]:
        """
        Get the web elements for articles on the specified page number.

        Args:
            page_number (int): The page number to get articles from.

        Returns:
            list[Any]: A list of web elements for the articles.

        Raises:
            Exception: If an error occurs while getting the web 
            elements.
        """
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
        """
        Get the article details from the web element.

        Args:
            article_web_element (Any): The web element of the article.
            article_number (int): The article number on the page.
            page_number (int): The page number of the article.

        Returns:
            Article: The Article object with the extracted details.

        Raises:
            Exception: If an error occurs while extracting the article 
            details.
        """
        try:
            # Define locators
            title_locator: str = 'class:promo-title'
            description_locator: str = 'class:promo-description'
            date_locator: str = 'class:promo-timestamp'
            image_locator: str = 'class:image'
            title: str = self.__handler.find_element(
                title_locator, parent=article_web_element
                ).text
            description: str = self.__handler.find_element(
                description_locator, parent=article_web_element
                ).text
            unconverted_date: str = self.__handler.find_element(
                date_locator, parent=article_web_element
                ).text
            
            date_handler: DateHandler = DateHandler()
            date: datetime = date_handler.convert_date_to_datetime(
                unconverted_date
                )
            image_src: str = self.__handler.find_element(
                image_locator, parent=article_web_element
                ).get_attribute('src')
            article = Article(title, date, description, image_src)
            return article
        except Exception as e:
            if "Element with locator 'class:image' not found" in str(e):
                warning_message: str = (
                    f'Image not found for article {article_number} in page '
                    f'{page_number}'
                )
                self.__log('warning', warning_message)
                print(warning_message)
                article = Article(title, date, description, 'Not found')
                return article
            error_message: str = (
                f'An error occurred while getting values for article '
                f'{article_number} in page {page_number}: {e}'
            )
            self.__log('error', error_message)
            raise

    def get_articles(self, search_phrase: str,
                     page_number: int) -> SearchArticleList:
        """
        Get the articles from the LA Times website that match the search
        phrase.

        Args:
            search_phrase (str): The phrase to search for in articles.
            page_number (int): The page number to get articles from.

        Returns:
            SearchArticleList: A list of articles that match the search 
            criteria.

        Raises:
            Exception: If an error occurs while getting the articles.
        """
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
        """
        Move to the next page of articles.

        Args:
            current_page_number (int): The current page number.

        Returns:
            bool: True if the navigation to the next page is successful,
            False otherwise.

        Raises:
            Exception: If an error occurs while moving to the next page.
        """
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
        """
        Close the browser.

        Returns:
            None

        Raises:
            Exception: If an error occurs while closing the browser.
        """
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

    def _get_handler(self) -> Selenium:
        """
        Get the Selenium handler.

        Returns:
            Selenium: The Selenium handler.
        """
        return self.__handler

    def __get_topic_web_elements(self) -> list[Any]:
        """
        Get the web elements for the topics on the search results page.

        Returns:
            A list of web elements (that are the topics)
        """
        try:
            topic_section_locator: str = "//*[@data-name='Topics']"
            self.__handler.wait_until_element_is_visible(
                topic_section_locator, timeout=30
                )
            topic_section_web_element: Any = self.__handler.find_element(
                topic_section_locator
                )
            topic_locator: str = 'tag:li'
            topic_section_web_elements: Any = self.__handler.find_elements(
                topic_locator, parent=topic_section_web_element
                )
            return topic_section_web_elements
        except Exception as e:
            error_message: str = (
                f'An error occurred when getting the web elements for the '
                f'search topics: {e}'
            )
            self.__log('error', error_message)
            raise

    def select_topic(self, topic: str) -> bool:
        try:
            self.__log('info', f'Selecting topic {topic}...')
            topic_web_elements: Any = self.__get_topic_web_elements()
            for topic_web_element in topic_web_elements:
                topic_title = self.__handler.find_element(
                    'tag:span', parent=topic_web_element 
                    ).text.lower()
                if topic_title == topic.lower():
                    checkbox = self.__handler.find_element(
                        'tag:input', parent=topic_web_element 
                        )
                    is_selected = self.__handler.is_checkbox_selected(checkbox)
                    if is_selected:
                        return True
                    self.__handler.click_element_when_clickable(
                        checkbox, timeout=30
                        )
                    self.__log('info', f'Finished selecting topic {topic}')
                    articles_section_locator: str = (
                        'class:search-results-module-results-menu'
                        )
                    self.__handler.wait_until_element_is_not_visible(
                        articles_section_locator, timeout=1
                        )
                    selected_topic_locator: str = (
                        'class:search-results-module-filters-selected'
                        )
                    self.__handler.wait_until_element_is_visible(
                        selected_topic_locator, timeout=30
                        )
                    return True
            self.__log('warning', f'Was not able to find topic: {topic}')
            print(f'Was not able to find topic: {topic}')
            return False
        except Exception as e:
            if 'still visible after' in str(e):
                return True
            error_message: str = (
                f'An error occurred while selecting topic {topic}: {e}'
            )
            self.__log('error', error_message)
            raise 