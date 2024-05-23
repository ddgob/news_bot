"""
This module defines the NewsWebsiteArticleScraper abstract base class, which 
provides an interface for scraping articles from a news website within a 
specified date range and matching a given search phrase.

Classes:
    NewsWebsiteArticleScraper: An abstract base class that defines the 
    interface for scraping articles within a date range and search phrase.
"""

from abc import ABC, abstractmethod
from datetime import datetime

from ..news_website_browser_service import NewsWebsiteBrowserService
from ..articles.article_list import SearchArticleList


class NewsWebsiteArticleScraper(ABC):
    """
    Abstract base class for scraping articles from a news website.

    This class provides an interface for scraping articles within a 
    specified date range that match a given search phrase.
    """

    @abstractmethod
    def scrape_search_articles_within_date_range(self, start_date: datetime,
                                                 end_date: datetime,
                                                 search_phrase: str,
                                                 browser_handler: NewsWebsiteBrowserService,
                                                 topic: str) -> SearchArticleList:
        """
        Scrape articles from the news website within the specified date 
        range that match the search phrase.

        Args:
            start_date (datetime): The start date for the date range.
            end_date (datetime): The end date for the date range.
            search_phrase (str): The phrase to search for in articles.
            handler (NewsWebsiteBrowserService): The browser service 
            handler to use for scraping.

        Returns:
            SearchArticleList: A list of articles that match the search 
            criteria.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """
