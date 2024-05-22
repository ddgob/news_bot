from .news_website_article_scraper import NewsWebsiteArticleScraper


class NewsWebsiteArticleScraperFactory:
    @staticmethod
    def create(website_url: str) -> NewsWebsiteArticleScraper:
        if website_url == 'https://www.latimes.com/':
            from .la_times_article_scraper import LATimesArticleScraper
            return LATimesArticleScraper()
        else:
            raise ValueError(
                f'No article scraper available for website {website_url}'
                )