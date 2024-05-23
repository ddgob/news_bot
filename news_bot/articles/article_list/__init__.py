"""
This module initializes the `article_list` package and defines the public 
interface for the package. It includes the ArticleList and SearchArticleList 
classes.

Modules:
    article_list: A list to manage Article objects.
    search_article_list: A specialized list to manage SearchArticle objects 
    with additional functionality specific to search phrases.

__all__:
    ArticleList: A list to manage Article objects.
    SearchArticleList: A list to manage SearchArticle objects with additional 
    functionality specific to search phrases.
"""

from .article_list import ArticleList
from .search_article_list import SearchArticleList

__all__ = ['ArticleList', 'SearchArticleList']
