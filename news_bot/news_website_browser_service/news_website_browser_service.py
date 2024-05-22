from .news_website_browser_handler_factory import NewsWebsiteBrowserHandlerFactory

class NewsWebsiteBrowserService:
    """
    Service class for handling browser interactions with a news website.
    """

    def __init__(self, website_url: str):
        """
        Initialize the NewsWebsiteBrowserService.

        Args:
            website_url (str): The URL of the news website to interact 
            with.
        """
        self.news_website_browser_handler = NewsWebsiteBrowserHandlerFactory.create(
            website_url
            )
        
    def open_website(self) -> None:
        """
        Open the news website in a browser.

        Returns:
            None
        """
        self.news_website_browser_handler.open_website()

    def search(self, phrase: str) -> None:
        """
        Search for articles on the news website using the specified 
        phrase.

        Args:
            phrase (str): The search phrase to use.

        Returns:
            None
        """
        self.news_website_browser_handler.search(phrase)

    def select_newest_articles(self) -> None:
        """
        Select the newest articles on the news website.

        Returns:
            None
        """
        self.news_website_browser_handler.select_newest_articles()

    def close_browser(self) -> None:
        """
        Close the browser.

        Returns:
            None
        """
        self.news_website_browser_handler.close_browser()

    def _get_handler(self):
        """
        Get the browser handler used by this service.

        Returns:
            The browser handler used by this service.
        """
        return self.news_website_browser_handler._get_handler()