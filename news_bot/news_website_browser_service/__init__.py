"""
This module initializes the `news_website_browser_service` package and 
defines the public interface for the package. It includes the 
NewsWebsiteBrowserService, NewsWebsiteBrowserHandler, LATimesBrowserHandler, and
NewsWebsiteBrowserHandlerFactory classes.

Modules:
    news_website_browser_service: A service for handling browser 
    interactions with a news website.
    la_times_browser_handler: A browser handler for scraping articles from 
    the LA Times website.
    news_website_browser_handler: An abstract base class for handling browser 
    interactions with a news website.
    news_website_browser_handler_factory: A factory class for creating 
    instances of NewsWebsiteBrowserHandler based on the website URL.

__all__:
    NewsWebsiteBrowserService: A service class for handling browser 
    interactions with a news website.
    NewsWebsiteBrowserHandler: An abstract base class for handling browser 
    interactions with a news website.
    LATimesBrowserHandler: A browser handler for scraping articles from 
    the LA Times website.
    NewsWebsiteBrowserHandlerFactory: A factory class for creating 
    instances of NewsWebsiteBrowserHandler based on the website URL.
"""

from .news_website_browser_service import NewsWebsiteBrowserService
from .la_times_browser_handler import LATimesBrowserHandler

__all__ = ['NewsWebsiteBrowserService', 'LATimesBrowserHandler']
