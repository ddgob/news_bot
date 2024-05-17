from RPA.Browser.Selenium import Selenium

class LATimesScraper:

    def __init__(self, phrase):
        self.browser = Selenium()
        self.phrase = phrase

    def close_browser(self):
        try:
            self.browser.close_all_browsers()
            print('Browser closed')
        except Exception as e:
            print(f"An error occurred closing the browser: {e}")
    
    def open_webiste(self):
        try:
            self.browser.open_available_browser('https://www.latimes.com/')
            print('Website succesfully opened')
        except Exception as e:
            print(f"An error occurred opening the website: {e}")

    def click_search_button(self):
        try:
            search_button_xpath = '//*[@data-element="search-button"]'
            self.browser.wait_until_page_contains_element(search_button_xpath)
            search_button = self.browser.find_element(search_button_xpath)
            self.browser.click_element(search_button, "ENTER")
            print('Search button clicked')
        except Exception as e:
            print(f"An error occurred when clicking search button: {e}")

    def search_frase(self):
        try:
            search_bar_xpath = '//input[@data-element="search-form-input"]'
            self.browser.wait_until_page_contains_element(search_bar_xpath)
            search_bar = self.browser.find_element(search_bar_xpath)
            self.browser.input_text(search_bar, self.phrase)
            self.browser.press_keys(search_bar, "ENTER")
            print('Phrase searched')
        except Exception as e:
            print(f"An error occurred when searching for phrase: {e}")

    def search_phrase(self):
        self.click_search_button()
        self.search_frase()

    def select_newest_articles(self):
        try:
            dropdown_xpath = '//select[@name="s"]'
            self.browser.wait_until_page_contains_element(dropdown_xpath)
            dropdown = self.browser.find_element(dropdown_xpath)
            self.browser.select_from_list_by_label(dropdown, "Newest")
            print('Newest articles selected')
        except Exception as e:
            print(f"An error occurred when selecting the newest articles: {e}")

    def run(self):
        self.open_webiste()
        self.search_phrase()
        self.select_newest_articles()
        self.close_browser()

if __name__ == '__main__':
    scraper = LATimesScraper('Covid')
    scraper.run()