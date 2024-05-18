import time
from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime, timedelta
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP

class LATimesScraper:

    def __init__(self, phrase, excel_path, images_directory_path, start_date, end_date):
        self.browser = Selenium()
        self.phrase = phrase
        self.news_data = []
        self.excel = Files()
        self.excel_path = excel_path
        self.http = HTTP()
        self.images_directory_path = images_directory_path
        # Start date should include entire day
        self.start_date = self.convert_date_to_datetime(start_date) + timedelta(hours=24)
        self.end_date = self.convert_date_to_datetime(end_date)
        self.ensure_end_date_earlier_than_start_date()

    def ensure_end_date_earlier_than_start_date(self):
        if self.start_date < self.end_date:
            self.start_date, self.end_date = self.end_date, self.start_date

    def close_browser(self):
        try:
            self.browser.close_all_browsers()
            print('Browser closed')
        except Exception as e:
            print(f'An error occurred closing the browser: {e}')
    
    def open_webiste(self):
        try:
            self.browser.open_available_browser('https://www.latimes.com/')
            print('Website opened')
        except Exception as e:
            print(f'An error occurred opening the website: {e}')

    def search_phrase(self):
        self.browser.click_element_when_clickable("//*[@data-element='search-button']")
        self.browser.input_text_when_element_is_visible("//input[@data-element='search-form-input']", self.phrase)
        self.browser.click_element_when_clickable("//*[@data-element='search-submit-button']")
        print('Phrase searched')

    def select_newest_articles(self):
        try:
            dropdown_xpath = "//select[@name='s']"
            self.browser.wait_until_element_is_visible(dropdown_xpath)
            self.browser.select_from_list_by_label(dropdown_xpath, 'Newest')
            self.browser.wait_until_element_is_visible(dropdown_xpath)
            print('Newest articles selected')
        except Exception as e:
            print(f'An error occurred when selecting the newest articles: {e}')
            
    def get_articles_from_current_page(self):
        try:
            print('Getting articles from current page')
            article_list_class = 'class:search-results-module-results-menu'
            self.browser.wait_until_element_is_visible(article_list_class)
            article_list = self.browser.find_element(article_list_class)
            articles = self.browser.find_elements('tag:li', parent=article_list)
            print('Got articles')
            return articles
        except Exception as e:
            print(f'An error occurred when getting articles from current page: {e}')
            return []

    def extract_image_filename(self, img_src):
        parsed_url = urlparse(img_src)
        query_params = parse_qs(parsed_url.query)
        image_url = query_params.get('url', [None])[0]
        if image_url:
            # Extract the file name
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
    
    def download_article_image(self, url, path_image_file):
        try:
            self.http.download(url, path_image_file)
        except Exception as e:
            print(f'An error occurred when downloading article image: {e}')

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
            print(f'Scraping values in article {article_number} from page {page_number}...')
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
                'description': description,
                'date': date,
                'image_filename': image_filename,
                'total_phrase_count': total_phrase_count,
                'contains_money': contains_money
            }
            print(f'Scraped values in article {article_number} from page {page_number}')
            return article_values, image_url
        except Exception as e:
            print(f'An error occurred when extracting article values: {e}')
    
    def log_article_values(self, article_values, article_number, page_number):
        print(f'Page number: {page_number}')
        print(f'Article number: {article_number}')
        print(f"Title: {article_values['title']}")
        print(f"Description: {article_values['description']}")
        print(f"Date: {article_values['date']}")
        print(f"Total phrase count in title and description: {article_values['total_phrase_count']}")
        print(f"Image filename: {article_values['image_filename']}")
        print(f"If title or description contain money amount: {article_values['contains_money']}")
        print('---')

    def scrape_valid_articles(self):
        try:
            page_number = 0
            print('----------- Start Article Log -----------')
            is_article_earlier_than_end_date = False
            # Iterates through pages, stops when finds 
            # article that is earlier than end date
            while True:
                articles = self.get_articles_from_current_page()
                # Iterates through articles in the current page
                for article_number, article in enumerate(articles):
                    article_values, image_url = self.scrape_article_values(article, article_number, page_number)
                    print(f'Verifying if article {article_number} from page {page_number} is valid')
                    # Breaks if article is after valid date range
                    if article_values['date'] < self.end_date:
                        is_article_earlier_than_end_date = True
                        break
                    # Skips articles that are before valid date range
                    if article_values['date'] > self.start_date:
                        continue
                    print(f'Verified article {article_number} from page {page_number} as valid')
                    # Store article values
                    self.news_data.append(article_values)
                    self.log_article_values(article_values, article_number, page_number)
                    #self.download_article_image(image_url, f"{self.images_directory_path}/{article_values['image_filename']}")
                if is_article_earlier_than_end_date:
                    break
                # Click on button to go to the next page of articles
                next_button_locator = f"css:a[href*='https://www.latimes.com/search?q={self.phrase}&s=1&p={page_number+2}']"
                self.browser.click_element_when_clickable(next_button_locator)
                time.sleep(10)
                page_number += 1
            print('----------- End Article Log -----------')
            print('All valid articles scraped')
        except Exception as e:
            print(f'An error occurred when extracting article content: {e}')

    def store_article_values_in_excel(self):
        try:
            formatted_start_date = self.start_date.strftime('%m-%d-%Y')
            formatted_end_date = self.end_date.strftime('%m-%d-%Y')
            worksheet_name = f'News search results for {self.phrase} from {formatted_start_date} to {formatted_end_date}'
            self.excel.create_workbook(self.excel_path, sheet_name=worksheet_name)
            self.excel.append_rows_to_worksheet([
                ["Title", "Date", "Description", "Picture Filename", "Count of Phrases", "Contains Money"]
            ], worksheet_name)
            self.excel.append_rows_to_worksheet(self.news_data, name=worksheet_name)
            self.excel.save_workbook()
        except Exception as e:
            print(f'An error occurred when storing article values in excel: {e}')

    def run(self):
        print('Opening website...')
        self.open_webiste()
        print('Searching phrase...')
        self.search_phrase()
        print('Selecting newest articles...')
        self.select_newest_articles()
        time.sleep(1)
        print('Scraping valid articles...')
        self.scrape_valid_articles()
        print('Storing article values in excel...')
        self.store_article_values_in_excel()
        print('Closing browser...')
        self.close_browser()

if __name__ == '__main__':
    scraper = LATimesScraper('Dollar', 'excel_file.xlsx', 'article_images', '05/17/2024', '05/16/2024')
    scraper.run()