from abc import ABC, abstractmethod

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