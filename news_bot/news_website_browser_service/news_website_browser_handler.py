from abc import ABC, abstractmethod

from RPA.Browser.Selenium import Selenium

class NewsWebsiteBrowserHandler(ABC):
    """
    Abstract base class for handling browser interactions with a news 
    website.

    This class provides an interface for interacting with a news website 
    using a browser, including opening the website, performing searches,
    selecting articles, and closing the browser.
    """

    @abstractmethod
    def open_website(self) -> None:
        """
        Open the news website in a browser.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """
        pass

    @abstractmethod
    def search(self, phrase: str) -> None:
        """
        Search for articles on the news website using the specified 
        phrase.

        Args:
            phrase (str): The search phrase to use.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """
        pass

    @abstractmethod
    def select_newest_articles(self) -> None:
        """
        Select the newest articles on the news website.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """
        pass

    def close_browser(self) -> None:
        """
        Close the browser.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """
        pass

    def _get_handler(self) -> Selenium:
        """
        Get the Selenium browser handler used by this service.

        Returns:
            Selenium: The Selenium browser handler.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """
        pass