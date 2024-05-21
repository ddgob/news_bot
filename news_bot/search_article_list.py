from .article_list import ArticleList
from .article import Article
from .article.search_article import SearchArticle
from datetime import datetime

class SearchArticleList(ArticleList):
    def __init__(self, search_phrase: str) -> None:
        super().__init__()
        self.__search_phrase: str = search_phrase

    def __iter__(self):
        return iter(self._get_articles())

    def append(self, article_to_append: Article) -> None:
        #_articles: list[Article] = self._get_articles()
        article: Article = article_to_append
        if not isinstance(article, Article):
            raise ValueError(
                'When trying to append an object to a ArticleList, that '
                'object must be of type Article or a subclass of Article'
            )
        if not isinstance(article, SearchArticle):
            article = SearchArticle.from_article(article, self.__search_phrase)
        if article.get_search_phrase() is not self.__search_phrase:
            raise ValueError(
                'When trying to append a SearchArticle object to a '
                'SearchArticleList, that SearchArticle must have the same '
                'search_phrase as the SearchArticleList'
            )
        super().append(article)

    def extend(self, articles: ArticleList) -> None:
        for article in articles:
            self.append(article)

    def convert_to_list_of_dict(self) -> list[dict]:
        list_of_dict: list[dict] = []
        for article in self._get_articles():
            search_article = SearchArticle.from_article(article, 
                                                        self.__search_phrase
                                                        )
            search_article.convert_to_dict()
            list_of_dict.append(search_article.convert_to_dict())
        return list_of_dict
    
    def filter_articles_within_date_range(self, start_date: datetime, 
                                   end_date: datetime) -> 'SearchArticleList':
        articles_within_date_range = SearchArticleList(self.__search_phrase)
        for article in self._get_articles():
            if not article.is_between_dates(start_date, end_date):
                continue
            articles_within_date_range.append(article)
        return articles_within_date_range