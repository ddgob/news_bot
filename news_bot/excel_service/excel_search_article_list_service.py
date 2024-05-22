from ..articles.article_list import SearchArticleList
from .excel_handler import ExcelHandler


class ExcelSearchArticleListService:
    def __init__(self) -> None:
        self.__excel_handler = ExcelHandler()


    def save_search_article_list_to_excel_file(self, 
                                               articles: SearchArticleList, 
                                               excel_file_name: str, 
                                               worksheet_name: str) -> None:
        list_of_dict_articles = articles.convert_to_list_of_dicts()
        self.__excel_handler.convert_list_of_dicts_to_excel_file(
            list_of_dict_articles, excel_file_name, worksheet_name
            )
