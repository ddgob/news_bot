"""
This module defines the ExcelSearchArticleListService class, which is a 
service for saving a list of search articles to an Excel file. It uses the 
ExcelHandler to convert and save articles.

Classes:
    ExcelSearchArticleListService: A service class for saving a list of 
    search articles to an Excel file.
"""

from ..articles.article_list import SearchArticleList
from .excel_handler import ExcelHandler


class ExcelSearchArticleListService:
    """
    Service class for saving a list of search articles to an Excel file.
    """

    def __init__(self) -> None:
        """
        Initialize the ExcelSearchArticleListService.

        Sets up the Excel handler for converting and saving articles to 
        an Excel file.
        """
        self.__excel_handler = ExcelHandler()


    def save_search_article_list_to_excel_file(self,
                                               articles: SearchArticleList,
                                               excel_file_name: str,
                                               worksheet_name: str) -> None:
        """
        Save the search article list to an Excel file.

        Args:
            articles (SearchArticleList): The list of search articles to
            save.
            excel_file_name (str): The name of the Excel file to save 
            the articles to.
            worksheet_name (str): The name of the worksheet within the 
            Excel file.

        Returns:
            None
        """
        list_of_dict_articles = articles.convert_to_list_of_dicts()
        self.__excel_handler.convert_list_of_dicts_to_excel_file(
            list_of_dict_articles, excel_file_name, worksheet_name
            )
