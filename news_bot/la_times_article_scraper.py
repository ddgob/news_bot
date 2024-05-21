from datetime import datetime
from .articles.article_list import SearchArticleList
from .la_times_browser_handler import LATimesBrowserHandler
from .logger import Logger
from typing import Any


class LATimesArticleScraper:
    def __init__(self) -> None:
        self.__log = Logger().log

    def scrape_search_articles_within_date_range(self, start_date: datetime, 
                                                  end_date: datetime, 
                                                  search_phrase: str,
                                                  handler: LATimesBrowserHandler
                                                  ) -> SearchArticleList:
        try:
            browser_handler: LATimesBrowserHandler = LATimesBrowserHandler(handler)
            articles_within_date_range: SearchArticleList = SearchArticleList(
                search_phrase
            )
            page_number: int = 1
            while True:
                articles: SearchArticleList = browser_handler.get_articles(
                    search_phrase, page_number
                    )
                valid_articles: SearchArticleList = articles.filter_articles_within_date_range(
                    start_date, end_date
                    )
                articles_within_date_range.extend(valid_articles)
                if articles.is_all_articles_before_date(start_date):
                    break
                if not browser_handler.move_to_next_article_page(page_number):
                    break
                page_number += 1
            return articles_within_date_range
        except Exception as e:
            if page_number == 10:
                warning_message: str = (
                    f'Reached end of available search results while scraping '
                    f'before reaching the date {start_date} for search phrase '
                    f'{search_phrase}: {e}'
                )
                self.__log('warning', warning_message)
                return articles_within_date_range
            error_message: str = (
                f'An error occurred while scraping articles within date range '
                f'{start_date} to {end_date} for search phrase '
                f'{search_phrase}: {e}'
            )
            self.__log('error', error_message)
            raise