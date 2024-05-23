"""
This module defines the ExcelSearchArticleListService class, which is a 
service for saving a list of search articles to an Excel file. It uses the 
ExcelHandler to convert and save articles.

Classes:
    ExcelSearchArticleListService: A service class for saving a list of 
    search articles to an Excel file.
"""

from datetime import datetime

from ..articles.article_list import SearchArticleList
from .excel_handler import ExcelHandler
from ..utils import Logger
from ..utils import DateHandler


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
        self.__log = Logger().log


    def save_search_article_list_to_excel_file(self,
                                               articles: SearchArticleList,
                                               excel_file_name: str,
                                               search_phrase: str,
                                               datetime_start_date: datetime,
                                               datetime_end_date: datetime,
                                               topic: str) -> None:
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
        date_handler = DateHandler()
        formatted_datetime_start_date = date_handler.convert_datetime_to_string(
            datetime_start_date, separator='-'
            )
        formatted_datetime_end_date = date_handler.convert_datetime_to_string(
            datetime_end_date, separator='-'
            )
        worksheet_name = (
            f'{search_phrase}_{formatted_datetime_start_date}_'
            f'{formatted_datetime_end_date}'
        )
        list_of_dict_articles = articles.convert_to_list_of_dicts()
        if len(list_of_dict_articles) == 0:
            warning_message = (
                f'No articles were found for the search phrase '
                f'{search_phrase} in the topic {topic} within the date range '
                f'{datetime_start_date} to {datetime_end_date}. Excel file '
                f'will not be created.'
            )
            self.__log('warning', warning_message)
            print(warning_message)
            return
        self.__excel_handler.convert_list_of_dicts_to_excel_file(
            list_of_dict_articles, excel_file_name, worksheet_name
            )
