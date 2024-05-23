"""
This module defines the NewsWebsiteBrowserHandler abstract base class, which 
provides an interface for handling browser interactions with a news website 
using Selenium. The class includes methods for opening the website, 
performing searches, selecting the newest articles, and closing the browser.

Classes:
    NewsWebsiteBrowserHandler: An abstract base class for handling browser 
    interactions with a news website. Subclasses must implement methods for 
    opening the website, performing searches, and selecting the newest 
    articles.
"""

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

    @abstractmethod
    def select_newest_articles(self) -> None:
        """
        Select the newest articles on the news website.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """

    def close_browser(self) -> None:
        """
        Close the browser.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """

    def _get_handler(self) -> Selenium:
        """
        Get the Selenium browser handler used by this service.

        Returns:
            Selenium: The Selenium browser handler.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """

    def select_topic(self, topic: str) -> bool:
        """
        Select a topic on the news website.

        Args:
            topic (str): The topic to select.
        
        Returns:
            bool: True if the topic was selected successfully, False 
            otherwise.

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass.
        """
