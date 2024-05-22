from RPA.Browser.Selenium import Selenium

from .news_website_browser_handler import NewsWebsiteBrowserHandler


class NewsWebsiteBrowserHandlerFactory:
    """
    Factory class to create an instance of NewsWebsiteBrowserHandler 
    based on the provided website URL.
    """

    @staticmethod
    def create(website_url: str) -> NewsWebsiteBrowserHandler:
        """
        Create an instance of NewsWebsiteBrowserHandler based on the 
        website URL.

        Args:
            website_url (str): The URL of the news website for which a 
            browser handler is needed.

        Returns:
            NewsWebsiteBrowserHandler: An instance of a concrete 
            subclass of NewsWebsiteBrowserHandler.

        Raises:
            ValueError: If no browser handler is available for the given
            website URL.
        """
        if website_url == 'https://www.latimes.com/':
            from .la_times_browser_handler import LATimesBrowserHandler
            return LATimesBrowserHandler(Selenium())
        else:
            raise ValueError(
                f'No browser handler available for website {website_url}'
                )