"""
This module provides functionality for interacting with the LA Times 
website using Selenium and saving the extracted articles to an Excel 
file. 

Classes:
    Excel: Handles creation and manipulation of Excel files.
    LATimesBrowser: Interacts with the LA Times website, searches for 
                    articles, and extracts article details.
    Scraper: Scrapes articles based on a given date range and search phrase.

Dependencies:
    - RPA.Excel.Files
    - RPA.Browser.Selenium
    - SeleniumLibrary.errors
    - logging
    - sys
    - datetime
    - typing
    - re
"""

import re
import logging
import sys
from datetime import datetime
from typing import Optional

from RPA.Excel.Files import Files
from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.errors import ElementNotFound

from news_bot.utils import DateUtil, ImageUtil

logger = logging.getLogger(__name__)

class Excel:
    """
    A class to handle the creation and manipulation of Excel files.

    This class provides methods to create a workbook, add rows to a 
    worksheet, and save the workbook to a specified directory. It uses 
    the `Files` class to handle the actual file operations.
    """

    def __init__(self) -> None:
        self.excel: Files = Files()

    def save_articles_excel(self, articles: list[dict],
                         excel_dir: str) -> None:
        """
        Saves a list of articles to an Excel file.

        This method takes a list of articles, each represented as a 
        dictionary, and saves them into an Excel file. It creates a 
        workbook, adds the articles to the specified worksheet, and then
        saves and closes the workbook. If the list of articles is empty,
        a warning is logged and no Excel file is created.

        Args:
            articles (list[dict]): A list of articles to be saved, where
                                   each article is represented as a 
                                   dictionary.
            excel_dir (str): The directory where the Excel file will be 
                             saved.

        Returns:
            None
        """
        logger.info('Saving articles to Excel...')
        worksheet_name: str = 'search_results'
        if len(articles) == 0:
            warning_message: str = (
                'No articles were found. Excel file will not be created.'
                )
            logger.warning(warning_message)
            return
        self.excel.create_workbook(excel_dir, sheet_name=worksheet_name)
        header: list[str] = list(articles[0].keys())
        self.excel.append_rows_to_worksheet([header], worksheet_name)
        self.excel.append_rows_to_worksheet(articles, worksheet_name)
        self.excel.save_workbook()
        self.excel.close_workbook()
        logger.info('Finished saving articles to Excel.')


class LATimesBrowser:
    """
    Singleton class for interacting with the LA Times website using 
    Selenium.

    This class provides methods for opening the website, searching for 
    articles, selecting topics, navigating pages, and extracting 
    article details. It ensures only one instance of the browser is 
    created and maintained throughout the usage of the class.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of LATimesBrowser if one does not 
        already exist.

        This method implements the singleton pattern by checking if an 
        instance already exists. If it does, it returns the existing 
        instance. Otherwise, it creates a new instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            LATimesBrowser: The singleton instance of LATimesBrowser.
        """
        if cls._instance is None:
            super_class = super(LATimesBrowser, cls)
            cls._instance = super_class.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the LATimesBrowser instance.

        This method initializes the Selenium browser and sets the base 
        URL for the LA Times website. It ensures that the 
        initialization is performed only once, even if the constructor 
        is called multiple times.
        """
        if not hasattr(self, 'initialized'):
            self.browser: Selenium = Selenium()
            self.initialized = True
            self.url = 'https://www.latimes.com/'

    def open_website(self) -> None:
        """
        Opens the LA Times website using the Selenium browser.

        This method logs the process of opening the website, opens the
        LA Times website using a Selenium browser instance, and logs
        the completion of the process.

        Returns:
            None
        """
        logger.info('Opening website...')
        self.browser.open_available_browser(self.url)
        logger.info('Finished opening website.')

    def search(self, phrase: str) -> None:
        """
        Searches for articles using the given search phrase on the LA 
        Times website.

        This method logs the search process, interacts with the search 
        button and input field on the website using Selenium, and 
        handles exceptions that may occur during the search input. If 
        the search input is not visible, it attempts to reopen the 
        website and retry the search. If a critical error occurs, it 
        logs the error and exits the program.

        Args:
            phrase (str): The search phrase to input into the search 
                          field.

        Returns:
            None
        """
        logger.info('Searching for articles...')
        search_button: str = "//*[@data-element='search-button']"
        self.browser.click_element_when_clickable(search_button, timeout=30)
        try:
            search_input: str = "//input[@data-element='search-form-input']"
            self.browser.input_text_when_element_is_visible(search_input,
                                                            phrase)
        except Exception as e:
            if 'not visible' in str(e):
                self.open_website()
                self.browser.click_element_when_clickable(search_button,
                                                          timeout=30)
                self.browser.input_text_when_element_is_visible(search_input,
                                                                phrase)
            else:
                critical_message: str = (
                    'A critical error occurred while inputting search phrase: '
                    '%s'
                    )
                logger.critical(critical_message, e)
                sys.exit(1)
        submit_button: str = "//*[@data-element='search-submit-button']"
        self.browser.click_element_when_clickable(submit_button, timeout=30)
        logger.info('Finished searching for articles.')

    def select_newest_articles(self) -> None:
        """
        Selects the newest articles on the LA Times website.

        This method interacts with the sort dropdown on the LA Times 
        website to select and display the newest articles. It waits for 
        the sort dropdown to become visible, selects the 'Newest' 
        option, and then waits for the articles section to update. If 
        there is an issue while waiting for the articles to load, it 
        logs a critical error and exits the program.

        Returns:
            None
        """
        logger.info('Selecting newest articles...')
        sort_by_dropdown: str = "//select[@name='s']"
        self.browser.wait_until_element_is_visible(sort_by_dropdown,
                                                   timeout=30)
        self.browser.select_from_list_by_label(sort_by_dropdown, 'Newest')
        self.__wait_for_articles_to_load()
        logger.info('Finished selecting newest articles.')

    def __wait_for_articles_to_load(self):
        """
        Waits for the articles section to start and finish loading on 
        the LA Times website.

        This method first waits for the articles section to become not 
        visible, indicating that loading has started. If an exception 
        occurs during this wait, it checks if the exception is because 
        the articles were already visible, in which case it does 
        nothing and proceeds. If any other exception occurs, it logs a 
        critical error and exits the program. After ensuring that 
        loading has started, it waits for the articles section to 
        become visible again, indicating that loading has finished.

        Raises:
            SystemExit: If an unexpected error occurs while waiting for 
                        articles to load.
        
        Returns:
            None
        """
        try:
            # Wait for the article section to start loading
            articles_section = 'class:search-results-module-results-menu'
            self.browser.wait_until_element_is_not_visible(articles_section,
                                                           timeout=1)
        except Exception as e:
            if 'still visible after' in str(e):
                # Case where articles finished loading before the
                # wait_until_element_is_not_visible command in the try
                # block was executed
                pass
            elif 'stale element reference' in str(e):
                # Case where articles are loading and the element
                # reference becomes stale
                pass
            else:
                critical_message = (
                    'An error occurred while waiting for articles to load: %s'
                    )
                logger.critical(critical_message, e)
                sys.exit(1)
        # Check if articles finished loading
        self.browser.wait_until_element_is_visible(articles_section,
                                                   timeout=30)

    def select_topic(self, search_topic: str) -> None:
        """
        Selects a specific topic on the LA Times website.

        This method iterates through the available topics on the LA 
        Times website, identifies the topic that matches the given 
        search topic, and selects it. If the topic title is not found 
        or does not match, it continues to the next topic. If no 
        matching topic is found, it logs a critical error and exits the 
        program.

        Args:
            search_topic (str): The topic to be searched and selected.

        Returns:
            None
        """
        logger.info('Selecting topic...')
        # Click see all button to see all topics
        see_all_button = "//*[@data-toggle-trigger='see-all']"
        self.browser.click_element_when_clickable(see_all_button, timeout=30)
        topics = self.__get_topics()
        # Iterate through topics to find the search topic
        for topic in topics:
            try:
                topic_title_locator: str = 'tag:span'
                topic_title: str = self.browser.find_element(
                    topic_title_locator, parent=topic).text.lower()
            except ElementNotFound:
                logger.error('Topic title not found. Moving to next topic.')
                continue
            # Check if the topic matches the search topic
            if topic_title == search_topic.lower():
                self.__check_topic_checkbox(topic)
                logger.info('Finished selecting topic.')
                return
        critical_message: str = 'Was not able to find topic: %s'
        logger.critical(critical_message, search_topic)
        sys.exit(1)

    def __get_topics(self):
        """
        Retrieves the list of topic elements from the LA Times website.

        This method waits for the topic section to become visible, 
        finds the topic section element, and retrieves all topic 
        elements within that section. If the topic section element is 
        not found, it logs a critical error and exits the program.

        Returns:
            list: A list of topic elements found within the topic 
                  section.
        """
        topic_section: str = "//*[@data-name='Topics']"
        self.browser.wait_until_element_is_visible(topic_section, timeout=30)
        try:
            topic_section_element = self.browser.find_element(topic_section)
        except ElementNotFound:
            logger.critical('Topic section element not found.')
            sys.exit(1)
        topics: str = 'tag:li'
        topic_elements = self.browser.find_elements(
            topics, parent=topic_section_element)
        return topic_elements

    def __check_topic_checkbox(self, topic: str) -> None:
        """
        Selects the checkbox for a given topic and verifies the 
        selection.

        This method finds the checkbox associated with the given topic, 
        checks if it is already selected, and if not, selects it. It 
        then verifies that the topic is selected and ensures the 
        articles for the selected topic are visible. If any critical 
        error occurs during these steps, it logs the error and exits 
        the program.

        Args:
            topic (str): The topic element to be selected.

        Returns:
            None
        """
        # Find the checkbox for the topic
        try:
            checkbox_locator: str = 'tag:input'
            checkbox = self.browser.find_element(checkbox_locator,
                                                 parent=topic)
        except ElementNotFound:
            logger.critical('Checkbox not found.')
            sys.exit(1)
        # Check if the topic is already selected
        if self.browser.is_checkbox_selected(checkbox):
            logger.warning('Topic is already selected.')
            return
        # Select the topic (if not already selected)
        self.browser.click_element_when_clickable(checkbox, timeout=30)
        # Make sure the topic is filtered
        try:
            topic_filter: str = (
                'class:search-results-module-filters-selected'
                )
            self.browser.wait_until_element_is_visible(topic_filter,
                                                       timeout=30)
        except Exception as e:
            if 'not visible' in str(e):
                self.browser.click_element_when_clickable(checkbox, timeout=30)
            else:
                critical_message: str = (
                    'An error occurred while verifying if topic was properly '
                    'selected: %s'
                    )
                logger.critical(critical_message, e)
                sys.exit(1)
        self.__wait_for_articles_to_load()

    def get_page_articles(self, phrase: str) -> list[dict]:
        """
        Retrieves articles from the current page and converts them to a 
        list of dictionaries.

        This method finds all article elements on the current page, 
        converts each article element to a dictionary using a helper 
        method, and returns a list of these dictionaries.

        Args:
            phrase (str): The search phrase to be used in article 
            conversion.

        Returns:
            list[dict]: A list of dictionaries, each representing an 
            article found on the page.
        """
        article_elements = self.__get_article_elements()
        articles: list = []
        for article_element in article_elements:
            article: dict = self.__article_element_to_dict(article_element,
                                                           phrase)
            articles.append(article)
        return articles

    def __get_article_elements(self):
        """
        Retrieves the list of article elements from the current page.

        This method waits for the article section to become visible, 
        finds the article section element, and retrieves all article 
        elements within that section. If the article section element is 
        not found, it logs an error and exits the program.

        Returns:
            list: A list of article elements found within the article 
                  section.
        """
        article_section: str = 'class:search-results-module-results-menu'
        self.browser.wait_until_element_is_visible(article_section, timeout=30)
        try:
            article_section_element = self.browser.find_element(
                article_section)
        except ElementNotFound:
            logger.error('Article section element not found.')
            sys.exit(1)
        articles: str = 'tag:li'
        article_elements = self.browser.find_elements(
            articles, parent=article_section_element)
        return article_elements

    def __article_element_to_dict(self, article_web_element,
                                  phrase:str) -> dict:
        """
        Converts a web element representing an article into a 
        dictionary.

        This method extracts various details from the given article web 
        element,such as the title, description, date, and image source. 
        It also checks if the article text contains any mention of 
        money and counts how many times the search phrase appears in 
        the article.

        Args:
            article_web_element: The web element representing the 
                                 article.
            phrase (str): The search phrase used to count its 
                          occurrences in the article.

        Returns:
            dict: A dictionary containing the article details, 
                  including title, description, date, image source, 
                  whether the text contains a mention of money, and the 
                  count of the search phrase.
        """
        title: str = self.__get_article_title(article_web_element)
        description: str = self.__get_article_description(article_web_element)
        date: str = self.__get_article_date(article_web_element)
        image_src: str = self.__get_article_image_src(article_web_element)
        image_file_name: str = self.__get_image_file_name(image_src)
        article_text: str = title + ' | ' + description
        text_contains_money: bool = self.__is_contains_money(article_text)
        phrase_count: int = article_text.count(phrase.lower())
        article: dict = {
            'title': title,
            'description': description,
            'date': date,
            'image_src': image_src,
            'image_file_name': image_file_name,
            'text_contains_money': text_contains_money,
            'search_phrase_count': phrase_count
        }
        return article

    def __get_article_title(self, article_web_element) -> str:
        """
        Extracts the title of an article from the given article web 
        element.

        This method finds the title element within the given article 
        element and returns the text content of that element. If the 
        title element is not found, it logs an error and returns a 
        placeholder string.

        Args:
            article_element: The web element representing the article.

        Returns:
            str: The title of the article or a placeholder string.
        """
        try:
            title_locator: str = 'class:promo-title'
            title: str = self.browser.find_element(
                title_locator, parent=article_web_element
                ).text
        except ElementNotFound:
            title: str = 'Title not found'
            error_message: str = (
                'Title element not found. Returned %s placeholder '
                'instead.'
                )
            logger.error(error_message, title)
        return title

    def __get_article_description(self, article_web_element) -> str:
        """
        Extracts the description of an article from the given article 
        web element.

        This method finds the description element within the given 
        article element and returns the text content of that element. If 
        the description element is not found, it logs an error and 
        returns a placeholder string.

        Args:
            article_element: The web element representing the article.

        Returns:
            str: The description of the article or a placeholder string.
        """
        try:
            description_locator: str = 'class:promo-description'
            description: str = self.browser.find_element(
                description_locator, parent=article_web_element
                ).text
        except ElementNotFound:
            description: str = 'Description not found'
            error_message: str = (
                'Description element not found. Returned %s placeholder '
                'instead.'
                )
            logger.error(error_message, description)
        return description

    def __get_article_date(self, article_web_element) -> str:
        """
        Extracts the date of an article from the given article web 
        element.

        This method finds the date element within the given article 
        element and returns the text content of that element. If the 
        date element is not found, it logs an error and returns a 
        placeholder string.

        Args:
            article_element: The web element representing the article.

        Returns:
            str: The date of the article or a placeholder string.
        """
        try:
            date_locator: str = 'class:promo-timestamp'
            unconverted_date: str = self.browser.find_element(
                date_locator, parent=article_web_element
                ).text
            date: Optional[datetime] = DateUtil.date_to_datetime(
                unconverted_date
                )
            if date is None:
                formatted_date: str = 'Date found but is empty'
                error_message: str = (
                    'Date element found but contains empty string. Returned '
                    '%s placeholder instead.'
                    )
                logger.error(error_message, formatted_date)
            else:
                formatted_date: str = date.strftime('%m/%d/%Y')
        except ElementNotFound:
            date: str = 'Date not found'
            error_message: str = (
                'Date element not found. Returned %s placeholder instead.'
                )
            logger.error(error_message, date)
        return formatted_date

    def __get_article_image_src(self, article_web_element) -> str:
        """
        Extracts the image source URL of an article from the given 
        article web element.

        This method finds the image element within the given article 
        element and returns the value of the 'src' attribute of that 
        element. If the image element is not found or does not have a 
        'src' attribute, it logs an error and returns a placeholder 
        string.

        Args:
            article_element: The web element representing the article.

        Returns:
            str: The image source URL of the article or a placeholder 
                 string.
        """
        try:
            image_locator: str = 'class:image'
            image_src: str = self.browser.find_element(
                image_locator, parent=article_web_element
                ).get_attribute('src')
        except ElementNotFound:
            image_src: str = 'Image not found'
            error_message: str = (
                'Image element not found. Returned %s placeholder instead.'
                )
            logger.error(error_message, image_src)
        return image_src

    def __get_image_file_name(self, image_src: str) -> str:
        """
        Extracts the image file name from the given image source URL.

        This method extracts the file name from the image source URL by 
        splitting the URL and returning the last part of the split. If 
        the image source URL is not valid, it logs an error and returns 
        a placeholder string.

        Args:
            image_src (str): The image source URL.

        Returns:
            str: The image file name or a placeholder string.
        """
        if image_src == 'Image not found':
            image_file_name: str = 'Image not found'
        else:
            image_file_name: str = ImageUtil.extract_image_name(image_src)
        return image_file_name

    def __is_contains_money(self, article_text: str):
        """
        Checks if the given article text contains a mention of money.

        This method uses a regular expression pattern to search for 
        money-related terms in the given text. If a match is found, it 
        returns True; otherwise, it returns False.

        Args:
            text (str): The text to search for money-related terms.

        Returns:
            bool: True if the text contains a mention of money, False 
                  otherwise.
        """
        money_pattern = (
            r'\$\d{1,3}((,?\d{3})|(\d*))*(\.\d{1,2})?'
            r'|(\d{1,3}(,?\d{3})*(\.\d{1,2})? (dollars|USD))'
        )
        if re.search(money_pattern, article_text.lower()):
            return True
        return False

    def next_page(self, page_number: int) -> bool:
        """
        Navigates to the next page of search results if available.

        This method attempts to navigate to the next page of search 
        results. If the page number is 10, it logs a warning that there 
        are only 10 pages of results and returns False. It waits for 
        the next button to be visible and clickable. If the next button 
        or its parent element is not found, it logs an error and 
        returns False. If successful, it clicks the next button and 
        returns True.

        Args:
            page_number (int): The current page number.

        Returns:
            bool: True if navigation to the next page is successful, 
                  False otherwise.
        """
        if page_number == 10:
            warning_message: str = (
                'Could not move to next page %d due to search results only '
                'return 10 pages of results.'
            )
            logger.warning(warning_message, page_number + 1)
            return False
        next_button_parent: str = 'class:search-results-module-next-page'
        self.browser.wait_until_element_is_visible(next_button_parent,
                                                   timeout=30)
        try:
            next_button_parent_element = self.browser.find_element(
                next_button_parent)
        except ElementNotFound:
            logger.error('Next button parent element not found.')
            return False
        try:
            next_button: str = 'tag:a'
            next_button_element = self.browser.find_element(
                next_button, parent=next_button_parent_element)
        except ElementNotFound:
            logger.error('Next button element not found.')
            return False
        self.browser.click_element_when_clickable(next_button_element,
                                                  timeout=30)
        return True

    def close_browser(self) -> None:
        """
        Closes the browser and resets the singleton instance.

        This method logs the process of closing the browser, closes the 
        browser using the Selenium instance, resets the singleton 
        instance to None, and logs the completion of the process.

        Returns:
            None
        """
        logger.info('Closing browser...')
        self.browser.close_browser()
        self._instance = None
        logger.info('Finished closing browser.')


class Scraper:
    """
    A class for scraping articles from the LA Times website within a 
    specified date range.

    This class provides methods to scrape articles based on a given 
    date range and search phrase. It uses the LATimesBrowser to 
    navigate the website, retrieve articles, and filter them according 
    to the specified criteria.
    """

    def __init__(self) -> None:
        self.__browser = LATimesBrowser()

    def scrape_articles_in_date_range(self, start_date: datetime,
                                      end_date: datetime,
                                      phrase: str) -> list[dict]:
        """
        Scrapes articles within a specified date range from the 
        LA Times website.

        This method initializes the browser, scrapes articles page by 
        page, and filters them based on the given date range. If the 
        date of an article cannot be found or is outside the specified 
        range, the article is skipped. The method continues to scrape 
        and collect articles until no more pages are available or all 
        articles within the date range are collected.

        Args:
            start_date (datetime): The start date of the date range for 
                                   scraping articles.
            end_date (datetime): The end date of the date range for 
                                 scraping articles.
            phrase (str): The search phrase to be used in filtering 
                          articles.

        Returns:
            list[dict]: A list of dictionaries, each representing an 
                        article found within the specified date range.
        """
        logger.info('Scraping articles...')
        page_number: int = 1
        articles: list = []
        while True:
            page_articles: list[dict] = self.__browser.get_page_articles(
                phrase)
            for page_article in page_articles:
                string_date: str = page_article['date']
                if string_date == 'Date not found':
                    warning_message: str = (
                        'Date not found for article when scraping. Therefore, '
                        'article will be skipped.'
                        )
                    logger.warning(warning_message)
                    continue
                page_article_date: Optional[datetime] = DateUtil.date_to_datetime(
                    string_date)
                if page_article_date > end_date:
                    continue
                if page_article_date < start_date:
                    if len(articles) == 0:
                        logger.warning('No articles found within date range.')
                    logger.info('Finished scraping articles.')
                    return articles
                articles.append(page_article)
            if not self.__browser.next_page(page_number):
                logger.info('Finished scraping articles.')
                return articles
            page_number += 1
