from abc import ABC, abstractmethod
from RPA.Browser.Selenium import Selenium

class NewsWebsiteBrowserHandler(ABC):
    @abstractmethod
    def open_website(self) -> None:
        pass

    @abstractmethod
    def search(self, phrase: str) -> None:
        pass

    @abstractmethod
    def select_newest_articles(self) -> None:
        pass

    def close_browser(self) -> None:
        pass

    def _get_handler(self) -> Selenium:
        pass