"""
This module initializes the `article` package and defines the public 
interface for the package. It includes the Article and SearchArticle classes.

Modules:
    article: Represents a news article with its title, date, description, 
    and image source.
    search_article: Represents a search article that extends the base 
    Article class, with additional functionality related to the search 
    phrase.

__all__:
    Article: Represents a news article with its title, date, description, 
    and image source.
    SearchArticle: Represents a search article that extends the base 
    Article class, with additional functionality related to the search 
    phrase.
"""

from .article import Article
from .search_article import SearchArticle

__all__ = ['Article', 'SearchArticle']
