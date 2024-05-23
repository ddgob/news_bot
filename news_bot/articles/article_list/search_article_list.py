"""
This module defines the SearchArticleList class, which is a specialized 
list for managing SearchArticle objects. It provides functionality specific 
to search phrases, including methods to append and extend the list, convert 
the list to a list of dictionaries, and filter articles within a specific 
date range.

Classes:
    SearchArticleList: A list to manage SearchArticle objects with 
    additional functionality specific to search phrases.
"""

from datetime import datetime

from news_bot.articles.article_list import ArticleList
from news_bot.articles.article import Article
from news_bot.articles.article import SearchArticle

class SearchArticleList(ArticleList):
    """
    A list to manage SearchArticle objects with additional functionality 
    specific to search phrases.
    """

    def __init__(self, search_phrase: str) -> None:
        """
        Initialize the SearchArticleList with a search phrase.

        Args:
            search_phrase (str): The search phrase associated with the 
            articles in the list.
        """
        super().__init__()
        self.__search_phrase: str = search_phrase

    def __iter__(self):
        """
        Return an iterator over the articles in the list.

        Returns:
            iterator: An iterator over the articles.
        """
        return iter(self._get_articles())

    def append(self, article_to_append: Article) -> None:
        """
        Append an article to the list.

        Args:
            article_to_append (Article): The article to append.

        Raises:
            ValueError: If the article is not of type Article or 
                        SearchArticle, or if the search phrase does not 
                        match.
        """
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
        """
        Extend the list by appending elements from another article list.

        Args:
            articles (ArticleList): The list of articles to append.

        Returns:
            None
        """
        for article in articles:
            self.append(article)

    def convert_to_list_of_dicts(self) -> list[dict]:
        """
        Convert the list of articles to a list of dictionaries.

        Returns:
            list[dict]: A list of dictionaries representing the 
            articles.
        """
        list_of_dict: list[dict] = []
        for article in self._get_articles():
            search_article = SearchArticle.from_article(article,
                                                        self.__search_phrase
                                                        )
            list_of_dict.append(search_article.convert_to_dict())
        return list_of_dict

    def filter_articles_within_date_range(self, start_date: datetime,
                                   end_date: datetime) -> 'SearchArticleList':
        """
        Filter the articles within a specific date range.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.

        Returns:
            SearchArticleList: A new SearchArticleList with articles 
            within the specified date range.
        """
        articles_within_date_range = SearchArticleList(self.__search_phrase)
        for article in self._get_articles():
            if not article.is_between_dates(start_date, end_date):
                continue
            articles_within_date_range.append(article)
        return articles_within_date_range
