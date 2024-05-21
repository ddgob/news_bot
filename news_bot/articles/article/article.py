from datetime import datetime
from ...url_handler import URLHandler
import re
from typing import Any


class Article:
    def __init__(
        self,
        title: str, 
        date: datetime, 
        description: str, 
        image_src: str
    ) -> None:
        self.__title: str = title
        self.__date: datetime = date
        self.__description: str = description
        self.__image_src: str = image_src

    def get_title(self) -> str:
        return self.__title

    def get_date(self) -> datetime:
        return self.__date

    def get_description(self) -> str:
        return self.__description

    def get_image_src(self) -> str:
        return self.__image_src

    def is_before_date(self, date: datetime) -> bool:
        return self.__date < date
    
    def is_between_dates(self, start_date: datetime, 
                         end_date: datetime) -> bool:
        return start_date <= self.__date <= end_date
    
    def get_image_file_name(self) -> str:
        url_handler: URLHandler = URLHandler()
        image_url = url_handler.get_image_url(self.__image_src)
        image_file_name = image_url.split('/')[-1]
        return image_file_name
    
    def is_contain_money_in_text(self) -> bool:
        money_regex_pattern = (
            r'\$\d{1,3}((,?\d{3})|(\d*))*(\.\d{1,2})?'
            r'|(\d{1,3}(,?\d{3})*(\.\d{1,2})? (dollars|USD))'
        )
        match_title: Any = re.search(money_regex_pattern, self.__title)
        match_description: Any = re.search(money_regex_pattern, 
                                           self.__description
                                           )
        if match_title or match_description:
            return True
        return False