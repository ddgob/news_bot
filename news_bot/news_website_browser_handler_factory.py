from .news_website_browser_handler import NewsWebsiteBrowserHandler
from RPA.Browser.Selenium import Selenium


class NewsWebsiteBrowserHandlerFactory:
    @staticmethod
    def create(website_url) -> NewsWebsiteBrowserHandler:
        if website_url == 'https://www.latimes.com/':
            from .la_times_browser_handler import LATimesBrowserHandler
            return LATimesBrowserHandler(Selenium())