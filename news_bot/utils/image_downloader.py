"""
This module provides the ImageDownloader class, which handles the 
downloading of images from URLs associated with articles. The class 
uses an HTTP client for downloading images and logs activities using 
a custom logger.
"""

from RPA.HTTP import HTTP

from .logger import Logger
from ..articles.article_list import ArticleList

class ImageDownloader:
    """
    A class to download images from URLs associated with articles.
    """

    def __init__(self) -> None:
        """
        Initialize the ImageDownloader.

        Sets up the logger for logging activities and initializes the 
        HTTP client.
        """
        self.__log = Logger().log
        self.__http: HTTP = HTTP()

    def is_image_file(self, image_name: str) -> bool:
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
        return image_name.lower().endswith(image_extensions)


    def download_image(self, image_url: str, images_dir: str,
                       image_name: str) -> None:
        """
        Download an image from the specified URL to the specified path.

        Args:
            image_url (str): The URL of the image to download.
            image_path (str): The local path where the image will be 
            saved.

        Raises:
            Exception: If an error occurs while downloading the image.
        """
        try:
            if image_url == 'not found':
                warning_message: str = (
                    'Will not download image due to image not found'
                )
                self.__log('warning', warning_message)
                print(warning_message)
                return
            self.__log('info', f'Downloading image from {image_url}...')
            if not self.is_image_file(image_name):
                image_name += '.jpg'
            image_path: str = f'{images_dir}/{image_name}'
            self.__http.download(image_url, image_path)
            self.__log('info', f'Finished downloading image from {image_url}')
        except Exception as e:
            error_message: str = (
                f'An error occurred while downloading image from {image_url}: '
                f'{e}'
            )
            self.__log('error', error_message)

    def download_images(self, articles: ArticleList, images_dir: str) -> None:
        """
        Download images for a list of articles.

        Args:
            articles (ArticleList): The list of articles containing 
            image URLs.
            images_dir (str): The directory where images will be saved.

        Returns:
            None
        """
        for article in articles:
            image_url: str = article.get_image_url()
            image_name: str = article.get_image_file_name()
            self.download_image(image_url, images_dir, image_name)
