from datetime import datetime

from ..article import Article


class ArticleList:
    def __init__(self) -> None:
        self.__articles: list[Article] = []

    def __iter__(self):
        return iter(self.__articles)

    def append(self, article: Article) -> None:
        if not isinstance(article, Article):
            raise ValueError(
                'When trying to append an object to an ArticleList, that '
                'object must be of type Article or a subclass of Article'
            )
        self.__articles.append(article)

    def _get_articles(self) -> list[Article]:
        return self.__articles

    def filter_articles_within_date_range(self, start_date: datetime, 
                                   end_date: datetime) -> 'ArticleList':
        articles_within_date_range: 'ArticleList' = ArticleList()
        for article in self.__articles:
            if not article.is_between_dates(start_date, end_date):
                continue
            articles_within_date_range.append(article)
        return articles_within_date_range
    
    def extend(self, articles: 'ArticleList') -> None:
        for article in articles:
            self.append(article)

    def is_all_articles_before_date(self, date: datetime) -> bool:
        return all(article.is_before_date(date) for article in self.__articles)