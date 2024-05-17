from RPA.Browser.Selenium import Selenium

class LATimesScraper:

    def __init__(self):
        self.browser = Selenium()

    def open_webiste(self):
        try:
            self.browser.open_available_browser('https://www.latimes.com/')
            print('Website succesfully opened')
        except Exception as e:
            print(f"An error occurred opening the website: {e}")

    def run(self):
        self.open_webiste()

if __name__ == '__main__':
    scraper = LATimesScraper()
    scraper.run()