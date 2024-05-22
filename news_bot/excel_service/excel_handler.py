from RPA.Excel.Files import Files
from ..logger import Logger
from datetime import datetime
from ..date_handler import DateHandler


class ExcelHandler:
    def __init__(self):
        self.__log = Logger().log
        self.__excel = Files()

    def convert_list_of_dicts_to_excel_file(self, 
                                                list_of_dicts: list[dict],
                                                excel_files_dir: str,
                                                worksheet_name: str):
        try:
            self.__log(
                'info', 
                f'Converting list of dictionaries to Excel file...'
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