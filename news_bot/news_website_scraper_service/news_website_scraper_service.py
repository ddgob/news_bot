"""
This module provides the NewsWebsiteScraperService class, which is used to 
scrape articles from a specified news website within a given date range. 
It utilizes the NewsWebsiteArticleScraperFactory to create an appropriate 
scraper for the website and the NewsWebsiteBrowserService to handle the 
browsing and scraping process.

Classes:
    NewsWebsiteScraperService: A service for scraping articles from a news 
    website within a specified date range and matching a given search phrase.
"""

from datetime import datetime

from .news_website_article_scraper_factory import NewsWebsiteArticleScraperFactory
from ..news_website_browser_service import NewsWebsiteBrowserService
from ..articles.article_list import SearchArticleList



class NewsWebsiteScraperService:
    """
    Service for scraping articles for a given topic from a news website within 
    a specified date range.
    """

    def __init__(self, website_url: str):
        """
        Initialize the NewsWebsiteScraperService.

        Args:
            website_url (str): The URL of the news website to scrape.
        """
        self.news_website_article_scraper = NewsWebsiteArticleScraperFactory.create(
            website_url
            )

    def scrape_search_articles_within_date_range(self, start_date: datetime,
                                                 end_date: datetime,
                                                 search_phrase: str,
                                                 handler: NewsWebsiteBrowserService,
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
            topic (str): The topic of the articles to search for.

        Returns:
            SearchArticleList: A list of articles that match the search 
            criteria.
        """
        return self.news_website_article_scraper.scrape_search_articles_within_date_range(
            start_date, end_date, search_phrase, handler, topic
            )
