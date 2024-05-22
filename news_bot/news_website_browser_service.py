from .news_website_browser_handler_factory import NewsWebsiteBrowserHandlerFactory

class NewsWebsiteBrowserService:
    def __init__(self, website_url: str):
        self.news_website_browser_handler = NewsWebsiteBrowserHandlerFactory.create(
            website_url
            )
        
    def open_website(self) -> None:
        self.news_website_browser_handler.open_website()

    def search(self, phrase: str) -> None:
        self.news_website_browser_handler.search(phrase)

    def select_newest_articles(self) -> None:
        self.news_website_browser_handler.select_newest_articles()

    def close_browser(self) -> None:
        self.news_website_browser_handler.close_browser()

    def _get_handler(self):
        return self.news_website_browser_handler._get_handler()