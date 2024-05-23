"""
This module defines the ExcelSearchArticleListService class, which is a 
service for saving a list of search articles to an Excel file. It uses the 
ExcelHandler to convert and save articles.

Classes:
    ExcelSearchArticleListService: A service class for saving a list of 
    search articles to an Excel file.
"""


from datetime import datetime

from RPA.Excel.Files import Files

from ..utils import Logger
from ..utils import DateHandler


class ExcelHandler:
    """
    Handler class for operations related to Excel files.
    """

    def __init__(self):
        """
        Initialize the ExcelHandler.

        Sets up the logger and the Excel file handler.
        """
        self.__log = Logger().log
        self.__excel = Files()

    def convert_list_of_dicts_to_excel_file(self,
                                                list_of_dicts: list[dict],
                                                excel_files_dir: str,
                                                worksheet_name: str) -> None:
        """
        Convert a list of dictionaries to an Excel file.

        Args:
            list_of_dicts (list[dict]): The list of dictionaries to 
            convert.
            excel_files_dir (str): The directory where the Excel file 
            will be saved.
            worksheet_name (str): The name of the worksheet within the 
            Excel file.

        Returns:
            None

        Raises:
            Exception: If an error occurs while converting the list of 
            dictionaries to an Excel file.
        """
        try:
            self.__log(
                'info', 
                'Converting list of dictionaries to Excel file...'
                )
            date_handler = DateHandler()
            now_date_string = date_handler.convert_datetime_to_string(
                datetime.now(), separator='-', is_show_time=True
            )
            excel_file_path = f'{excel_files_dir}/{now_date_string}.xlsx'
            self.__excel.create_workbook(excel_file_path, sheet_name=worksheet_name)
            header = list(list_of_dicts[0].keys())
            self.__excel.append_rows_to_worksheet([header], worksheet_name)
            self.__excel.append_rows_to_worksheet(list_of_dicts,
                                                  worksheet_name
                                                  )
            self.__excel.save_workbook()
            self.__excel.close_workbook()
            self.__log(
                'info', 
                'Finished converting list of dictionaries to Excel file...'
                )
        except Exception as e:
            error_message = (
                f'An error occurred while converting list of dictionaries to '
                f'Excel file: {e}'
            )
            self.__log('error', error_message)
