"""
This module initializes the `excel_search_article_list_service` package and 
defines the public interface for the package. It includes the 
ExcelSearchArticleListService class.

Modules:
    excel_search_article_list_service: A service for saving a list of 
    search articles to an Excel file.

__all__:
    ExcelSearchArticleListService: A service class for saving a list of 
    search articles to an Excel file.
"""

from .excel_search_article_list_service import ExcelSearchArticleListService

__all__ = ['ExcelSearchArticleListService']
