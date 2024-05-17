from RPA.Browser.Selenium import Selenium

class LATimesScraper:

    def __init__(self):
        self.browser = Selenium()

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

    def run(self):
        self.open_webiste()
        self.close_browser()

if __name__ == '__main__':
    scraper = LATimesScraper()
    scraper.run()