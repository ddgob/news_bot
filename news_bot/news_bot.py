"""
This module provides the NewsBot class which is used to scrape news articles
from a website based on a search phrase and date range. The scraped articles
are saved to an Excel file and associated images are downloaded.

The module imports various services and utilities to facilitate these tasks,
including logging, date handling, and HTTP requests.
"""

from .utils import Logger
from .news_website_browser_service import NewsWebsiteBrowserService
from .news_website_scraper_service import NewsWebsiteScraperService
from .excel_service import ExcelSearchArticleListService
from .utils import DateHandler
from .utils import ImageDownloader


class NewsBot:
    """
    A bot to scrape news articles from a website based on a search 
    phrase and date range.
    """

    def __init__(self) -> None:
        """
        Initialize the NewsBot.

        Sets up the logger for logging activities.
        """
        self.__log = Logger().log

    def scrape_articles_by_date_range(self, website_url: str,
                                      search_phrase: str, start_date: str,
                                      end_date: str,
                                      excel_files_dir: str,
                                      images_dir: str) -> bool:
        """
        Scrape news articles from the website within the specified date 
        range and save them to an Excel file and download associated 
        images.

        Args:
            website_url (str): The URL of the news website.
            search_phrase (str): The phrase to search for in articles.
            start_date (str): The start date for the date range 
            (MM/DD/YYYY).
            end_date (str): The end date for the date range (MM/DD/YYYY).
            excel_files_dir (str): The directory where the Excel file 
            will be saved.
            images_dir (str): The directory where the article images 
            will be saved.

        Returns:
            bool: True if the scraping and saving process was 
                    successful, 
                  False otherwise.

        Raises:
            Exception: If an error occurs during the scraping process.
        """
        try:
            date_handler = DateHandler()
            datetime_start_date, datetime_end_date = date_handler.first_date_earlier_than_second(
                start_date, end_date
                )
            datetime_end_date = date_handler.make_until_end_of_day(
                datetime_end_date
                )
            self.__log(
                'info', 
                f'Scraping articles within dates {datetime_start_date} and '
                f'{datetime_end_date} for search phrase: {search_phrase}...'
                )
            news_website_browser_service = NewsWebsiteBrowserService(
                website_url
            )
            news_website_browser_service.open_website()
            news_website_browser_service.search(search_phrase)
            news_website_browser_service.select_newest_articles()
            news_website_scraper_service = NewsWebsiteScraperService(
                website_url
            )
            articles = news_website_scraper_service.scrape_search_articles_within_date_range(
                datetime_start_date, datetime_end_date, search_phrase,
                news_website_browser_service
                )
            news_website_browser_service.close_browser()
            excel_search_article_list_service = ExcelSearchArticleListService()
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
            excel_search_article_list_service.save_search_article_list_to_excel_file(
                articles, excel_files_dir, worksheet_name
                )
            self.__log(
                'info', 
                f'Finished scraping articles within dates '
                f'{datetime_start_date} and {datetime_end_date} for search '
                f'phrase: {search_phrase}'
                )
            image_downloader = ImageDownloader()
            image_downloader.download_images(articles, images_dir)
            return True
        except Exception as e:
            self.__log(
                'error', 
                f'An error occured while scraping articles within dates '
                f'{datetime_start_date} and {datetime_end_date} for search '
                f'phrase {search_phrase}: {e}'
                )
            return False
