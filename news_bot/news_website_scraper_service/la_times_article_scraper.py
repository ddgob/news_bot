"""
This module defines the LATimesArticleScraper class, which is a concrete 
implementation of the NewsWebsiteArticleScraper abstract base class. It is 
used for scraping articles from the LA Times website within a specified date 
range and matching a given search phrase.

Classes:
    LATimesArticleScraper: A concrete implementation of 
    NewsWebsiteArticleScraper for scraping articles from the LA Times 
    website.
"""

from datetime import datetime

from ..articles.article_list import SearchArticleList
from ..news_website_browser_service import LATimesBrowserHandler
from ..utils import Logger
from .news_website_article_scraper import NewsWebsiteArticleScraper
from ..news_website_browser_service import NewsWebsiteBrowserService


class LATimesArticleScraper(NewsWebsiteArticleScraper):
    """
    Concrete implementation of NewsWebsiteArticleScraper for scraping 
    articles from the LA Times website.
    """

    def __init__(self) -> None:
        """
        Initialize the LATimesArticleScraper.

        Sets up the logger for logging activities.
        """
        self.__log = Logger().log

    def scrape_search_articles_within_date_range(self, start_date: datetime,
                                                 end_date: datetime,
                                                 search_phrase: str,
                                                 browser_handler: NewsWebsiteBrowserService,
                                                 topic: str) -> SearchArticleList:
        """
        Scrape articles for a given topic from the LA Times website within the 
        specified date range that match the search phrase.

        Args:
            start_date (datetime): The start date for the date range.
            end_date (datetime): The end date for the date range.
            search_phrase (str): The phrase to search for in articles.
            browser_handler (NewsWebsiteBrowserService): The browser 
            service handler to use for scraping.
            topic (str): The topic of the articles to search for.

        Returns:
            SearchArticleList: A list of articles that match the search 
            criteria.

        Raises:
            Exception: If an error occurs during the scraping process.
        """
        try:
            la_times_browser_handler: LATimesBrowserHandler = LATimesBrowserHandler(
                browser_handler._get_handler()
                )
            articles_within_date_range: SearchArticleList = SearchArticleList(
                search_phrase
            )
            page_number: int = 1
            while True:
                articles: SearchArticleList = la_times_browser_handler.get_articles(
                    search_phrase, page_number
                    )
                valid_articles: SearchArticleList = articles.filter_articles_within_date_range(
                    start_date, end_date
                    )
                articles_within_date_range.extend(valid_articles)
                # If all articles are before the start date, stop scraping
                if articles.is_an_article_before_date(start_date):
                    return articles_within_date_range
                if not la_times_browser_handler.move_to_next_article_page(page_number):
                    break
                page_number += 1
            return articles_within_date_range
        except Exception as e:
            if page_number == 10:
                warning_message: str = (
                    f'Reached end of available search results while scraping '
                    f'before reaching the date {start_date} for search phrase '
                    f'{search_phrase}: {e}'
                )
                self.__log('warning', warning_message)
                return articles_within_date_range
            error_message: str = (
                f'An error occurred while scraping articles within date range '
                f'{start_date} to {end_date} for search phrase '
                f'{search_phrase}: {e}'
            )
            self.__log('error', error_message)
            raise
