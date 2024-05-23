"""
This module initializes the `news_website_scraper_service` package and 
defines the public interface for the package. It includes the 
NewsWebsiteScraperService class.

Modules:
    news_website_scraper_service: A service for scraping articles from a 
    news website within a specified date range.

__all__:
    NewsWebsiteScraperService: A service class for scraping articles from 
    a news website within a specified date range.
"""

from .news_website_scraper_service import NewsWebsiteScraperService

__all__ = ['NewsWebsiteScraperService']
