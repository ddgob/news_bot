"""
This module provides classes and methods for scraping articles from the 
LA Times website.

It includes the following classes:
- LATimesNewsBot: A bot for scraping articles within a specified date 
                  range, search phrase and topic, saving the results to 
                  an Excel file, and downloading associated images.

The module uses the LATimesBrowser to navigate the website and retrieve 
articles, Excel to save the results, ImageUtil to download images and 
DateUtil for date conversions.

Dependencies:
- datetime
- logging
- news_bot.handlers.Excel
- news_bot.handlers.LATimesBrowser
- news_bot.handlers.Scraper
- news_bot.utils.DateUtil
- news_bot.utils.ImageUtil

Usage:
    Instantiate the LATimesNewsBot with the directory paths for Excel 
    and images, then call the get_articles method with the search 
    phrase, start date, end date, and topic.
"""

from datetime import datetime
import logging

from news_bot.handlers import Excel, LATimesBrowser, Scraper
from news_bot.utils import ImageUtil

logger = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class LATimesNewsBot:
    """
    A bot for scraping articles from the LA Times website within a 
    specified date range, search phrase and topic, 
    saving the results to an Excel file and downloading associated 
    images.

    This class provides run() method to perform searche on the LA Times 
    website, scrape articles, and save the results.

    Attributes:
        __excel_dir (str): Directory to save the Excel file with 
                           scraped articles.
        __images_dir (str): Directory to save the downloaded images.
    """

    def __init__(self, excel_dir: str, images_dir: str) -> None:
        self.__excel_dir = excel_dir
        self.__images_dir = images_dir

    def run(self, phrase: str, start_date: datetime,
                     end_date: datetime, topic: str) -> bool:
        """
        Retrieves articles from the LA Times website within a specified 
        date range and topic.

        This method prepares the dates, opens the LA Times website, 
        performs a search using the given phrase, selects the newest 
        articles, and filters them by the specified topic. It then 
        scrapes the articles within the date range, saves them to an 
        Excel file, and downloads associated images.

        Args:
            phrase (str): The search phrase to input into the search 
                          field.
            start_date (datetime): The start date string for the date 
                                   range.
            end_date (datetime): The end date string for the date range.
            topic (str): The topic to filter articles by.

        Returns:
            bool: True if the process completes successfully, False 
                  otherwise.
        """
        logger.info('Running news bot...')
        browser: LATimesBrowser = LATimesBrowser()
        browser.open_website()
        browser.search(phrase)
        browser.select_newest_articles()
        browser.select_topic(topic)
        scraper = Scraper()
        articles: list[dict] = scraper.scrape_articles_in_date_range(
            start_date, end_date, phrase
            )
        browser.close_browser()
        # Create list with all image sources
        image_src_list = [article['image_src'] for article in articles]
        # Remove 'image_src' from all articles
        for article in articles:
            del article['image_src']
        excel: Excel = Excel()
        excel.save_articles_excel(articles, self.__excel_dir)
        image_downloader = ImageUtil()
        image_downloader.download_images(image_src_list, self.__images_dir)
        logger.info('Finished running news bot.')
