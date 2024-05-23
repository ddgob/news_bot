"""
This module defines the SearchArticle class, which extends the base Article 
class. It adds additional functionality related to the search phrase used to 
find the article, including methods to create a SearchArticle from an 
existing Article, get the search phrase, count the occurrences of the search 
phrase in the article's title and description, and convert the article to a 
dictionary representation.

Classes:
    SearchArticle: Represents a search article that extends the base 
    Article class, with additional functionality related to the search 
    phrase.
"""

from datetime import datetime

from news_bot.articles.article import Article
from news_bot.utils import DateHandler


class SearchArticle(Article):
    """
    Represents a search article that extends the base Article class.

    This class adds additional functionality related to the search 
    phrase used to find the article.
    """

    def __init__(
        self,
        title: str,
        date: datetime,
        description: str,
        image_url: str,
        search_phrase: str
    ) -> None:
        """
        Initialize the SearchArticle.

        Args:
            title (str): The title of the article.
            date (datetime): The publication date of the article.
            description (str): The description of the article.
            image_url (str): The URL of the article's image.
            search_phrase (str): The search phrase used to find the 
            article.
        """
        super().__init__(title, date, description, image_url)
        self.__search_phrase: str = search_phrase

    @classmethod
    def from_article(cls, article: Article,
                     search_phrase: str) -> 'SearchArticle':
        """
        Create a SearchArticle from an existing Article.

        Args:
            article (Article): The existing article.
            search_phrase (str): The search phrase used to find the 
            article.

        Returns:
            SearchArticle: A new SearchArticle instance.
        """
        return cls(article.get_title(), article.get_date(),
                   article.get_description(), article.get_image_src(),
                   search_phrase
                   )

    def get_search_phrase(self) -> str:
        """
        Get the search phrase associated with the article.

        Returns:
            str: The search phrase.
        """
        return self.__search_phrase

    def get_search_phrase_count(self) -> int:
        """
        Get the count of the search phrase occurrences in the article's 
        title and description.

        Returns:
            int: The count of the search phrase occurrences.
        """
        search_phrase = self.get_search_phrase().lower()
        title = self.get_title().lower()
        description = self.get_description().lower()
        title_count = title.count(search_phrase)
        description_count = description.count(search_phrase)
        return title_count + description_count

    def convert_to_dict(self) -> dict:
        """
        Convert the article to a dictionary representation.

        Returns:
            dict: A dictionary representing the article's details.
        """
        date_handler: DateHandler = DateHandler()
        string_date: str = date_handler.convert_datetime_to_string(
            self.get_date()
            )
        return {
            'Title': self.get_title(),
            'Date': string_date,
            'Description': self.get_description(),
            'Image file name': self.get_image_file_name(),
            'Search phrase count in article text': self.get_search_phrase_count(),
            'Is article text contain money': self.is_contain_money_in_text()
        }
