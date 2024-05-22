from datetime import datetime

from news_bot.articles.article import Article
from ...utils import DateHandler


class SearchArticle(Article):
    def __init__(
        self,
        title: str, 
        date: datetime, 
        description: str, 
        image_url: str,
        search_phrase: str
    ) -> None:
        super().__init__(title, date, description, image_url)
        self.__search_phrase: str = search_phrase

    @classmethod
    def from_article(cls, article: Article, 
                     search_phrase: str) -> 'SearchArticle':
        return cls(article.get_title(), article.get_date(), 
                   article.get_description(), article.get_image_src(), 
                   search_phrase
                   )
    
    def get_search_phrase(self) -> str:
        return self.__search_phrase
    
    def get_search_phrase_count(self) -> str:
        search_phrase = self.get_search_phrase().lower()
        title = self.get_title().lower()
        description = self.get_description().lower()
        title_count = title.count(search_phrase)
        description_count = description.count(search_phrase)
        return title_count + description_count
    
    def convert_to_dict(self) -> dict:
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