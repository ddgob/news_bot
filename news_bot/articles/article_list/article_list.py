"""
This module defines the ArticleList class, which is used to manage a list of 
Article objects. It provides methods to append and extend the list, filter 
articles within a specific date range, and check if all articles are before 
a specified date.

Classes:
    ArticleList: A list to manage Article objects.
"""

from datetime import datetime

from news_bot.articles.article import Article


class ArticleList:
    """
    A list to manage Article objects.
    """

    def __init__(self) -> None:
        """
        Initialize the ArticleList.
        
        Sets up an empty list to store Article objects.
        """
        self.__articles: list[Article] = []

    def __iter__(self):
        """
        Return an iterator over the articles in the list.

        Returns:
            iterator: An iterator over the articles.
        """
        return iter(self.__articles)

    def append(self, article_to_append: Article) -> None:
        """
        Append an article to the list.

        Args:
            article (Article): The article to append.

        Raises:
            ValueError: If the article is not of type Article or its 
            subclass.
        """
        if not isinstance(article_to_append, Article):
            raise ValueError(
                'When trying to append an object to an ArticleList, that '
                'object must be of type Article or a subclass of Article'
            )
        self.__articles.append(article_to_append)

    def _get_articles(self) -> list[Article]:
        """
        Get the list of articles.

        Returns:
            list[Article]: The list of articles.
        """
        return self.__articles

    def filter_articles_within_date_range(self, start_date: datetime,
                                   end_date: datetime) -> 'ArticleList':
        """
        Filter the articles within a specific date range.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.

        Returns:
            ArticleList: A new ArticleList with articles within the 
            specified date range.
        """
        articles_within_date_range: 'ArticleList' = ArticleList()
        for article in self.__articles:
            if not article.is_between_dates(start_date, end_date):
                continue
            articles_within_date_range.append(article)
        return articles_within_date_range

    def extend(self, articles: 'ArticleList') -> None:
        """
        Extend the list by appending elements from another article list.

        Args:
            articles (ArticleList): The list of articles to append.

        Returns:
            None
        """
        for article in articles:
            self.append(article)

    def is_all_articles_before_date(self, date: datetime) -> bool:
        """
        Check if all articles are before the specified date.

        Args:
            date (datetime): The date to compare against.

        Returns:
            bool: True if all articles are before the specified date, 
            False otherwise.
        """
        return all(article.is_before_date(date) for article in self.__articles)
