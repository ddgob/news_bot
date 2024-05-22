from .news_website_article_scraper_factory import NewsWebsiteArticleScraperFactory
from datetime import datetime
from ..news_website_browser_service import NewsWebsiteBrowserService
from ..articles.article_list import SearchArticleList



class NewsWebsiteScraperService:
    def __init__(self, website_url: str):
        self.news_website_article_scraper = NewsWebsiteArticleScraperFactory.create(
            website_url
            )
        
    def scrape_search_articles_within_date_range(self, start_date: datetime, 
                                                 end_date: datetime, 
                                                 search_phrase: str,
                                                 handler: NewsWebsiteBrowserService
                                                 ) -> SearchArticleList:
        return self.news_website_article_scraper.scrape_search_articles_within_date_range(
            start_date, end_date, search_phrase, handler
            )