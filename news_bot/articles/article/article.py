from typing import Any
import re
from datetime import datetime

from ...utils import URLHandler


class Article:
    """
    Represents a news article with its title, date, description, and 
    image source.
    """

    def __init__(
        self,
        title: str, 
        date: datetime, 
        description: str, 
        image_src: str
    ) -> None:
        """
        Initialize the Article.

        Args:
            title (str): The title of the article.
            date (datetime): The publication date of the article.
            description (str): The description of the article.
            image_src (str): The source URL of the article's image.
        """
        self.__title: str = title
        self.__date: datetime = date
        self.__description: str = description
        self.__image_src: str = image_src

    def get_title(self) -> str:
        """
        Get the title of the article.

        Returns:
            str: The title of the article.
        """
        return self.__title

    def get_date(self) -> datetime:
        """
        Get the publication date of the article.

        Returns:
            datetime: The publication date of the article.
        """
        return self.__date

    def get_description(self) -> str:
        """
        Get the description of the article.

        Returns:
            str: The description of the article.
        """
        return self.__description

    def get_image_src(self) -> str:
        """
        Get the source URL of the article's image.

        Returns:
            str: The source URL of the article's image.
        """
        return self.__image_src

    def is_before_date(self, date: datetime) -> bool:
        """
        Check if the article's publication date is before a given date.

        Args:
            date (datetime): The date to compare against.

        Returns:
            bool: True if the article's publication date is before the 
            given date, False otherwise.
        """
        return self.__date < date
    
    def is_between_dates(self, start_date: datetime, 
                         end_date: datetime) -> bool:
        """
        Check if the article's publication date is within a given date 
        range.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.

        Returns:
            bool: True if the article's publication date is within the 
            date range, False otherwise.
        """
        return start_date <= self.__date <= end_date
    
    def get_image_url(self) -> str:
        """
        Get the resolved URL of the article's image.

        Returns:
            str: The resolved URL of the image.
        """
        url_handler: URLHandler = URLHandler()
        return url_handler.get_image_url(self.__image_src)
    
    def get_image_file_name(self) -> str:
        """
        Get the file name of the article's image.

        Returns:
            str: The file name of the image.
        """
        image_url = self.get_image_url()
        return image_url.split('/')[-1]
    
    def is_contain_money_in_text(self) -> bool:
        """
        Check if the article's title or description contains a monetary 
        value.

        Returns:
            bool: True if the title or description contains a monetary 
            value, False otherwise.
        """
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