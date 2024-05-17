import time
from urllib.parse import urlparse, parse_qs
import re
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files

class LATimesScraper:

    def __init__(self, phrase, excel_path):
        self.browser = Selenium()
        self.phrase = phrase
        self.news_data = []
        self.excel = Files()
        self.excel_path = excel_path

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

    def get_articles(self):
        try:
            time.sleep(10)
            article_list_xpath = 'xpath:/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/main/ul/li'
            self.browser.wait_until_page_contains_element('xpath:/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/main/ul')
            articles = self.browser.find_elements(article_list_xpath)
            print('Got articles')

            return articles
        except Exception as e:
            print(f'An error occurred when getting article: {e}')

    def extract_image_filename(self, img_src):
        parsed_url = urlparse(img_src)
        query_params = parse_qs(parsed_url.query)
        image_url = query_params.get('url', [None])[0]
        if image_url:
            # Extract the file name
            file_name = image_url.split('/')[-1]
            return file_name
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

    def extract_article_values(self):
        try:
            articles = self.get_articles()
            print('----------- Start Article Log -----------')
            for article_number, article in enumerate(articles):
                # Extract values
                title = self.browser.find_element('xpath:.//ps-promo/div/div[2]/div/h3/a', parent=article).text
                description = self.browser.find_element('xpath:.//ps-promo/div/div[2]/p[1]', parent=article).text
                date = self.browser.find_element('xpath:.//ps-promo/div/div[2]/p[2]', parent=article).text
                image_src = self.browser.find_element('xpath:.//ps-promo/div/div[1]/a/picture/img', parent=article).get_attribute('src')
                image_filename = self.extract_image_filename(image_src)
                total_phrase_count = self.is_phrase_in_article(title, description)
                contains_money = self.is_money_in_article(title, description)
                # Log extracted values
                print(f'Article number: {article_number}')
                print(f'Title: {title}')
                print(f'Description: {description}')
                print(f'Date: {date}')
                print(f'Total phrase count in title and description: {total_phrase_count}')
                print(f'Image filename: {image_filename}')
                print(f'If title or description contain money amount: {contains_money}')
                print('---')
                # Store values
                self.news_data.append({
                    "title": title,
                    "description": description,
                    "date": date,
                    "image_filename": image_filename,
                    "count_phrases": total_phrase_count,
                    "contains_money": contains_money
                })
            print('----------- End Article Log -----------')
        except Exception as e:
            print(f'An error occurred when extracting article values: {e}')

    def store_article_values_in_excel(self):
        worksheet_name = f'News search results for {self.phrase}'
        self.excel.create_workbook(self.excel_path, sheet_name=worksheet_name)
        self.excel.append_rows_to_worksheet([
            ["Title", "Date", "Description", "Picture Filename", "Count of Phrases", "Contains Money"]
        ], worksheet_name)
        self.excel.append_rows_to_worksheet(self.news_data, name=worksheet_name)
        self.excel.save_workbook()

    def run(self):
        print('Opening website...')
        self.open_webiste()
        print('Searching phrase...')
        self.search_phrase()
        print('Selecting newest articles...')
        self.select_newest_articles()
        print('Extracting article values...')
        self.extract_article_values()
        print('Storing article values in excel...')
        self.store_article_values_in_excel()
        print('Closing browser...')
        self.close_browser()

if __name__ == '__main__':
    scraper = LATimesScraper('Dollar', 'excel_file.xlsx')
    scraper.run()