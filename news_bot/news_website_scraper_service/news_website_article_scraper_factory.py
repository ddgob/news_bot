"""
This module contains the NewsWebsiteArticleScraperFactory class, which is 
responsible for creating instances of NewsWebsiteArticleScraper based on a 
provided website URL. The factory determines the appropriate scraper to 
instantiate for the given website.

Classes:
    NewsWebsiteArticleScraperFactory: A factory class for creating 
    instances of NewsWebsiteArticleScraper based on the website URL.
"""

from .news_website_article_scraper import NewsWebsiteArticleScraper
from .la_times_article_scraper import LATimesArticleScraper

class NewsWebsiteArticleScraperFactory:
    """
    Factory class to create an instance of NewsWebsiteArticleScraper 
    based on the provided website URL.
    """

    @staticmethod
    def create(website_url: str) -> NewsWebsiteArticleScraper:
        """
        Create an instance of NewsWebsiteArticleScraper based on the website 
        URL.

        Args:
            website_url (str): The URL of the news website for which an article
            scraper is needed.

        Returns:
            NewsWebsiteArticleScraper: An instance of a concrete subclass of 
            NewsWebsiteArticleScraper.

        Raises:
            ValueError: If no article scraper is available for the given 
            website URL.
        """
        if website_url == 'https://www.latimes.com/':
            return LATimesArticleScraper()
        else:
            raise ValueError(
                f'No article scraper available for website {website_url}'
                )
