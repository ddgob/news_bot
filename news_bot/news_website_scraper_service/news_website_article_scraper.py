from abc import ABC, abstractmethod
from datetime import datetime
from ..news_website_browser_service import NewsWebsiteBrowserService
from ..articles.article_list import SearchArticleList


class NewsWebsiteArticleScraper(ABC):
    @abstractmethod
    def scrape_search_articles_within_date_range(self, start_date: datetime, 
                                                 end_date: datetime, 
                                                 search_phrase: str, 
                                                 handler: NewsWebsiteBrowserService
                                                 ) -> SearchArticleList:
        pass