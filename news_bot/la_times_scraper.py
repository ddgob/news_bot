from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime, timedelta
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from .logger import Logger

class LATimesScraper:

    def __init__(self, phrase, excel_files_dir, article_images_dir, log_dir, start_date, end_date):
        self.browser = Selenium()
        self.phrase = phrase
        self.news_data = []
        self.excel = Files()
        self.excel_files_dir = excel_files_dir
        self.http = HTTP()
        self.article_images_dir = article_images_dir
        self.logger = Logger(log_dir).log
        # Start date should include entire day
        self.start_date = self.convert_date_to_datetime(start_date) + timedelta(hours=23, minutes=59, seconds=59)
        self.end_date = self.convert_date_to_datetime(end_date)
        self.ensure_end_date_earlier_than_start_date()

    def ensure_end_date_earlier_than_start_date(self):
        if self.start_date < self.end_date:
            self.start_date, self.end_date = self.end_date, self.start_date

    def close_browser(self):
        try:
            self.logger('info', 'Closing browser...')
            self.browser.close_all_browsers()
            self.logger('info', 'Finished closing browser')
        except Exception as e:
            self.logger('error', f'An error occurred while closing the browser: {e}')
    
    def open_webiste(self):
        try:
            self.logger('info', 'Opening website...')
            self.browser.open_available_browser('https://www.latimes.com/')
            self.logger('info', 'Finished opening website')
        except Exception as e:
            self.logger('error', f'An error occurred while opening the website: {e}')

    def search_phrase(self):
        try:
            self.logger('info', 'Searching phrase...')
            self.browser.click_element_when_clickable("//*[@data-element='search-button']", timeout=30)
            self.browser.input_text_when_element_is_visible("//input[@data-element='search-form-input']", self.phrase)
            self.browser.click_element_when_clickable("//*[@data-element='search-submit-button']", timeout=30)
            self.logger('info', 'Finished searching phrase')
        except Exception as e:
            self.logger('error', f'An error occurred while searching phrase: {e}')

    def select_newest_articles(self):
        try:
            self.logger('info', 'Selecting newest articles...')
            dropdown_xpath = "//select[@name='s']"
            self.browser.wait_until_element_is_visible(dropdown_xpath, timeout=30)
            self.browser.select_from_list_by_label(dropdown_xpath, 'Newest')
            # Wait for the newest articles to load
            self.browser.wait_until_element_is_not_visible('class:search-results-module-results-menu', timeout=1)
            self.logger('info', 'Finished selecting newest articles')
        except Exception as e:
            self.logger('error', f'An error occurred while selecting the newest articles: {e}')
            
    def get_articles_from_current_page(self, page_number):
        try:
            self.logger('info', f'Getting articles from page {page_number}...')
            article_list_class = 'class:search-results-module-results-menu'
            self.browser.wait_until_element_is_visible(article_list_class, timeout=30)
            article_list = self.browser.find_element(article_list_class)
            articles = self.browser.find_elements('tag:li', parent=article_list)
            self.logger('info', f'Finished getting articles from page {page_number}')
            return articles
        except Exception as e:
            self.logger('error', f'An error occurred when getting articles from page {page_number}: {e}')
            return []

    def extract_image_filename(self, img_src):
        parsed_url = urlparse(img_src)
        query_params = parse_qs(parsed_url.query)
        image_url = query_params.get('url', [None])[0]
        if image_url:
            file_name = image_url.split('/')[-1]
            return file_name, image_url
        return None

    def is_phrase_in_article(self, title, description):
        count_phrase_in_title = title.lower().count(self.phrase.lower())
        count_phrase_in_description = description.lower().count(self.phrase.lower())
        return count_phrase_in_title + count_phrase_in_description
    
    def is_money_in_article(self, title, description):
        money_regex_pattern = r'\$\d{1,3}((,?\d{3})|(\d*))*(\.\d{1,2})?|(\d{1,3}(,?\d{3})*(\.\d{1,2})? (dollars|USD))'
        match_title = re.search(money_regex_pattern, title)
        match_description = re.search(money_regex_pattern, description)
        contains_money = False
        if match_title or match_description:
            contains_money = True
        return contains_money
    
    def download_article_image(self, url, image_filename, article_number, page_number):
        try:
            self.logger('info', f'Downloading image in article {article_number} from page {page_number}: {image_filename}')
            self.http.download(url, f"{self.article_images_dir}/{image_filename}")
            self.logger('info', f'Finished downloading image in article {article_number} from page {page_number}: {image_filename}')
        except Exception as e:
            self.logger('error', f'An error occurred while downloading article image: {e}')

    def convert_date_to_datetime(self, date):
        current_time = datetime.now()
        # Pattern that matches MM/YY/YYYY
        input_date_regex_pattern = r'^(0?[1-9]|1[0-2])\/(0?[1-9]|[12][0-9]|3[01])\/[0-9]{4}$'
        # Pattern that matches <Month>. DD,YYYY
        article_date_regex_pattern = r'^[A-Za-z]+. [0-9]{1,2}, [0-9]{4}$'
        # Pattern that matches minute, minutes hour or hours
        minutes_ago_regex_pattern = re.compile(r'(\d+)\s+minutes?\s+ago')
        # Pattern that matches hour or hours
        hours_ago_regex_pattern = re.compile(r'(\d+)\s+hours?\s+ago')
        # Return datetime for pattern that is matched
        if re.search(input_date_regex_pattern, date):
            return datetime.strptime(date, '%m/%d/%Y')
        elif re.search(article_date_regex_pattern, date):
            return datetime.strptime(date.replace('.', ''), '%b %d, %Y')
        elif hours_match := hours_ago_regex_pattern.match(date):
            hours = int(hours_match.group(1))
            return current_time - timedelta(hours=hours)
        elif minutes_match := minutes_ago_regex_pattern.match(date):
            minutes = int(minutes_match.group(1))
            return current_time - timedelta(minutes=minutes)
        else:
            raise ValueError('Date pattern not recognized')
        
    def scrape_article_values(self, article, article_number, page_number):
        try:
            title = self.browser.find_element('class:promo-title', parent=article).text
            description = self.browser.find_element('class:promo-description', parent=article).text
            unconverted_date = self.browser.find_element('class:promo-timestamp', parent=article).text
            date = self.convert_date_to_datetime(unconverted_date)
            image_src = self.browser.find_element('class:image', parent=article).get_attribute('src')
            image_filename, image_url = self.extract_image_filename(image_src)
            total_phrase_count = self.is_phrase_in_article(title, description)
            contains_money = self.is_money_in_article(title, description)
            article_values = {
                'title': title,
                'date': date,
                'description': description,
                'image_filename': image_filename,
                'total_phrase_count': total_phrase_count,
                'contains_money': contains_money
            }
            return article_values, image_url
        except Exception as e:
            self.logger('error', f'An error occurred while scraping values in article {article_number} from page {page_number}: {e}')
            return None, None
    
    def print_article_values(self, article_values, article_number, page_number):
        print('---')
        print(f'Page number: {page_number}')
        print(f'Article number: {article_number}')
        print(f"Title: {article_values['title']}")
        print(f"Description: {article_values['description']}")
        print(f"Date: {article_values['date']}")
        print(f"Total phrase count in title and description: {article_values['total_phrase_count']}")
        print(f"Image filename: {article_values['image_filename']}")
        print(f"If title or description contain money amount: {article_values['contains_money']}")
        print('---')

    def navigate_to_next_page(self, page_number):
        try:
            next_page_div_class = 'class:search-results-module-next-page'
            self.browser.wait_until_element_is_visible(next_page_div_class, timeout=30)
            next_page_div = self.browser.find_element(next_page_div_class)
            next_page_button = self.browser.find_element('tag:a', parent=next_page_div)
            self.browser.click_element_when_clickable(next_page_button, timeout=30)
        except Exception as e:
            self.logger('critical', f'A critical error occurred while moving from page {page_number+1} to page {page_number+2}: {e}')
            raise

    def scrape_all_valid_articles(self):
        try:
            self.logger('info', 'Scraping all valid articles...')
            page_number = 0
            is_article_earlier_than_end_date = False
            # Iterates through pages, stops when finds 
            # article that is earlier than end date
            while True:
                articles = self.get_articles_from_current_page(page_number)
                self.logger('info', f'Scraping valid articles from page {page_number}...')
                # Iterates through articles in the current page
                for article_number, article in enumerate(articles):
                    article_values, image_url = self.scrape_article_values(article, article_number, page_number)
                    # Breaks if article is after valid date range
                    if article_values['date'] < self.end_date:
                        is_article_earlier_than_end_date = True
                        break
                    # Skips articles that are before valid date range
                    if article_values['date'] > self.start_date:
                        continue
                    # Convert date back to string type (to be visible in excel)
                    article_values['date'] = article_values['date'].strftime('%m/%d/%Y')
                    # Store article values
                    self.news_data.append(article_values)
                    #self.print_article_values(article_values, article_number, page_number)
                    #self.download_article_image(image_url, article_values['image_filename'], article_number, page_number)
                self.logger('info', f'Finished scraping valid articles from page {page_number}')
                if is_article_earlier_than_end_date:
                    break
                self.navigate_to_next_page(page_number)
                page_number += 1
            self.logger('info', 'Finished scraping all valid articles')
        except Exception as e:
            self.logger('error', f'An error occurred while scraping all valid articles: {e}')

    def store_article_values_in_excel(self):
        try:
            self.logger('info', 'Storing article values in excel...')
            formatted_start_date = self.start_date.strftime('%m-%d-%Y')
            formatted_end_date = self.end_date.strftime('%m-%d-%Y')
            worksheet_name = f'{self.phrase}_{formatted_start_date}-{formatted_end_date}'
            self.excel.create_workbook(f'{self.excel_files_dir}/{datetime.now()}.xlsx', sheet_name=worksheet_name)
            self.excel.append_rows_to_worksheet([
                ["Title", "Date", "Description", "Picture Filename", "Count of Phrases", "Contains Money"]
            ], worksheet_name)
            self.excel.append_rows_to_worksheet(self.news_data, name=worksheet_name)
            self.excel.save_workbook()
            self.logger('info', 'Finished storing article values in excel')
        except Exception as e:
            self.logger('error', f'An error occurred while storing article values in excel: {e}')

    def run(self):
        self.open_webiste()
        self.search_phrase()
        self.select_newest_articles()
        self.scrape_all_valid_articles()
        self.store_article_values_in_excel()
        self.browser.close_browser()