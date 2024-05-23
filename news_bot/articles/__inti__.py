"""
This module initializes the `article_management` package and defines the public 
interface for the package. It includes the Article, SearchArticle, ArticleList, 
and SearchArticleList classes.

Subpackages:
    article: Represents a news article with its title, date, description, 
    and image source.
    search_article: Represents a search article that extends the base 
    Article class, with additional functionality related to the search 
    phrase.
    article_list: A list to manage Article objects.
    search_article_list: A specialized list to manage SearchArticle objects 
    with additional functionality specific to search phrases.

__all__:
    Article: Represents a news article with its title, date, description, 
    and image source.
    SearchArticle: Represents a search article that extends the base 
    Article class, with additional functionality related to the search 
    phrase.
    ArticleList: A list to manage Article objects.
    SearchArticleList: A list to manage SearchArticle objects with additional 
    functionality specific to search phrases.
"""

from .article.article import Article
from .article.search_article import SearchArticle
from .article_list.article_list import ArticleList
from .article_list.search_article_list import SearchArticleList

__all__ = ['Article', 'SearchArticle', 'SearchArticleList', 'ArticleList']
