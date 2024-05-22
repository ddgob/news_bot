from RPA.Browser.Selenium import Selenium

from .news_website_browser_handler import NewsWebsiteBrowserHandler


class NewsWebsiteBrowserHandlerFactory:
    @staticmethod
    def create(website_url: str) -> NewsWebsiteBrowserHandler:
        if website_url == 'https://www.latimes.com/':
            from .la_times_browser_handler import LATimesBrowserHandler
            return LATimesBrowserHandler(Selenium())
        else:
            raise ValueError(
                f'No browser handler available for website {website_url}'
                )