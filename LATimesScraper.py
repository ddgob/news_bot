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
        self.verify_end_date_earlier_than_start_date()

    def verify_end_date_earlier_than_start_date(self):
        if self.start_date < self.end_date:
            temp_start_date = self.start_date
            self.start_date = self.end_date
            self.end_date = temp_start_date

    def close_browser(self):
        try:
            self.browser.close_all_browsers()
            print('Browser closed')
        except Exception as e:
            print(f'An error occurred closing the browser: {e}')
    
    def open_webiste(self):
        try:
            self.browser.open_available_browser('https://www.latimes.com/')
            print('Website succesfully opened')
        except Exception as e:
            print(f'An error occurred opening the website: {e}')

    def click_search_button(self):
        try:
            search_button_xpath = "//*[@data-element='search-button']"
            self.browser.wait_until_page_contains_element(search_button_xpath)
            search_button = self.browser.find_element(search_button_xpath)
            self.browser.click_element(search_button, 'ENTER')
            print('Search button clicked')
        except Exception as e:
            print(f'An error occurred when clicking search button: {e}')

    def search_frase(self):
        try:
            search_bar_xpath = "//input[@data-element='search-form-input']"
            self.browser.wait_until_page_contains_element(search_bar_xpath)
            search_bar = self.browser.find_element(search_bar_xpath)
            self.browser.input_text(search_bar, self.phrase)
            self.browser.press_keys(search_bar, 'ENTER')
            print('Phrase searched')
        except Exception as e:
            print(f'An error occurred when searching for phrase: {e}')

    def search_phrase(self):
        self.click_search_button()
        self.search_frase()

    def select_newest_articles(self):
        try:
            dropdown_xpath = "//select[@name='s']"
            self.browser.wait_until_page_contains_element(dropdown_xpath)
            dropdown = self.browser.find_element(dropdown_xpath)
            self.browser.select_from_list_by_label(dropdown, 'Newest')
            print('Newest articles selected')
        except Exception as e:
            print(f'An error occurred when selecting the newest articles: {e}')
            
    def get_articles_for_current_page(self):
        try:
            time.sleep(10)
            article_list_xpath = 'xpath:/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/main/ul/li'
            self.browser.wait_until_page_contains_element('xpath:/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/main/ul')
            articles = self.browser.find_elements(article_list_xpath)
            print('Got articles')
            return articles
        except Exception as e:
            print(f'An error occurred when getting article: {e}')
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
        # Pattern that matches <Month> DD,YYYY
        article_date_regex_pattern = r'^[A-Za-z]+ [0-9]{1,2}, [0-9]{4}$'
        # Pattern that matches minute, minutes hour or hours
        minutes_ago_regex_pattern = re.compile(r'(\d+)\s+minutes?\s+ago')
        # Pattern that matches hour or hours
        hours_ago_regex_pattern = re.compile(r'(\d+)\s+hours?\s+ago')
        # Return datetime for pattern that is matched
        if re.search(input_date_regex_pattern, date):
            return datetime.strptime(date, '%m/%d/%Y')
        elif re.search(article_date_regex_pattern, date):
            return datetime.strptime(date, '%B %d, %Y')
        elif hours_match := hours_ago_regex_pattern.match(date):
            hours = int(hours_match.group(1))
            return current_time - timedelta(hours=hours)
        elif minutes_match := minutes_ago_regex_pattern.match(date):
            minutes = int(minutes_match.group(1))
            return current_time - timedelta(minutes=minutes)
        else:
            raise ValueError('Date pattern not recognized')
        
    def extract_article_values(self, article):
        try:
            title = self.browser.find_element('xpath:.//ps-promo/div/div[2]/div/h3/a', parent=article).text
            description = self.browser.find_element('xpath:.//ps-promo/div/div[2]/p[1]', parent=article).text
            unconverted_date = self.browser.find_element('xpath:.//ps-promo/div/div[2]/p[2]', parent=article).text
            date = self.convert_date_to_datetime(unconverted_date)
            image_src = self.browser.find_element('xpath:.//ps-promo/div/div[1]/a/picture/img', parent=article).get_attribute('src')
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

    def extract_content_in_articles(self):
        try:
            page_number = 0
            print('----------- Start Article Log -----------')
            is_article_earlier_than_end_date = False
            # Iterates through pages, stops when finds 
            # article that is earlier than end date
            while True:
                articles = self.get_articles_for_current_page()
                # Iterates through articles in the current page
                for article_number, article in enumerate(articles):
                    article_values, image_url = self.extract_article_values(article)
                    # Breaks if article is after valid date range
                    if article_values['date'] < self.end_date:
                        is_article_earlier_than_end_date = True
                        break
                    # Skips articles that are before valid date range
                    if article_values['date'] > self.start_date:
                        continue
                    # Store article values
                    self.news_data.append(article_values)
                    self.log_article_values(article_values, article_number, page_number)
                    self.download_article_image(image_url, f"{self.images_directory_path}/{article_values['image_filename']}")
                if is_article_earlier_than_end_date:
                    break
                # Click on button to go to the next page of articles
                next_button_xpath = 'xpath:/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/main/div[2]/div[3]/a'
                self.browser.click_element_when_clickable(next_button_xpath)
                time.sleep(10)
                page_number += 1
            print('----------- End Article Log -----------')
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
        print('Extracting article values and image...')
        self.extract_content_in_articles()
        print('Storing article values in excel...')
        self.store_article_values_in_excel()
        print('Closing browser...')
        self.close_browser()

if __name__ == '__main__':
    scraper = LATimesScraper('Dollar', 'excel_file.xlsx', 'article_images', '05/17/2024', '05/16/2024')
    scraper.run()