"""
This module provides utility classes for handling image downloads and 
date conversions.

Classes:
    ImageUtil: A utility class for downloading images from URLs.
    DateUtil: A utility class for converting date strings to datetime 
              objects.
"""

from datetime import datetime, timedelta
import re
from urllib.parse import urlparse, parse_qs
import logging
from typing import Optional, Tuple

from RPA.HTTP import HTTP

logger = logging.getLogger(__name__)


class ImageUtil:
    """
    Utility class for downloading images from articles.

    It offers functionalities to:
      - Extract image names from URLs.
      - Download images from a list of sources to a specified 
        directory.

    This class utilizes an HTTP client (provided as an `HTTP` 
    attribute) to handle image downloads. 
    """

    def __init__(self) -> None:
        self.__http: HTTP = HTTP()

    @classmethod
    def extract_image_name(cls, image_src: str) -> Optional[str]:
        """
        Extracts and returns the image name from the given image source 
        URL.

        This method attempts to extract the image URL from the provided 
        image source using the `__get_image_url` method. If the URL is 
        invalid, it logs an error message and returns None. If the URL 
        is valid, it extracts the image name from the URL. If the image 
        name does not have a valid image extension, it appends '.jpg' 
        to the image name.

        Args:
            image_src (str): The image source URL.

        Returns:
            str: The image name with a valid extension if the 
                 extraction is successful, otherwise None.
        """
        image_url: Optional[str] = cls.__get_image_url(image_src)
        if image_url is None:
            error_message: str = (
                'Could not extract image name from an invalid image source '
                'URL.'
                )
            logger.error(error_message)
            return None
        image_name: str = image_url.split('/')[-1]
        if not cls.__is_image(image_name):
            image_name += '.jpg'
        return image_name

    def download_images(self, image_src_list: list[str],
                        images_dir: str) -> None:
        """
        Downloads images from a list of image sources to a specified 
        directory.

        This method iterates through the list of image sources, 
        attempts to download each image using the `___download_image` 
        method, and logs the progress. If an image download fails, it 
        logs an error message and continues to the next image.

        Args:
            image_src_list (list[str]): A list of image sources.
            images_dir (str): The directory where images will be 
                              downloaded.

        Returns:
            None
        """
        for num, image_src in enumerate(image_src_list, start=1):
            logger.info('Downloading image %d...', num)
            if not self.___download_image(image_src, images_dir):
                error_message: str = (
                    'Failed to download image %d. Skipping...'
                    )
                logger.error(error_message, num)
            info_message: str = (
                'Finished downloading process for image  %d. %d images left '
                'to download.'
                )
            logger.info(info_message, num, len(image_src_list) - num)

    @staticmethod
    def __get_image_url(image_src: str) -> Optional[str]:
        """
        Extracts the image URL from the given image source URL.

        This method parses the provided `image_src` URL and extracts 
        the value of the 'url' query parameter. If the 'url' query 
        parameter is not found, it logs an error message and returns 
        None.

        Args:
            image_src (str): The image source URL containing the image 
                             URL as a query parameter.

        Returns:
            str: The extracted image URL if found, otherwise None.
        """
        parsed_url = urlparse(image_src)
        query_params: dict[str, list[str]] = parse_qs(parsed_url.query)
        image_url: Optional[str] = query_params.get('url', [None])[0]
        if not image_url:
            error_message: str = (
                'No image URL found in the image source URL.'
                )
            logger.error(error_message)
            return None
        return image_url

    def ___download_image(self, image_src: str, images_dir: str) -> bool:
        """
        Downloads an image from the given image source URL and saves it 
        to the specified directory.

        This method extracts the image URL from the provided image 
        source using the `__get_image_url` method. If the URL is 
        invalid, it logs an error message and returns False. If the URL 
        is valid, it constructs the file path for the image, downloads 
        it using the HTTP class, and saves it to the specified 
        directory.

        Args:
            image_src (str): The image source URL.
            images_dir (str): The directory where the image will be 
                              saved.

        Returns:
            bool: True if the image was downloaded successfully, False 
                  otherwise.
        """
        image_url: str = self.__get_image_url(image_src)
        if image_url is None:
            error_message: str = (
                'Could not download image from an invalid image source URL.'
                )
            logger.error(error_message)
            return False
        image_path: str = f'{images_dir}/{self.extract_image_name(image_src)}'
        self.__http.download(image_url, image_path)
        return True

    @staticmethod
    def __is_image(image_name: str) -> bool:
        """
        Checks if the given file name corresponds to a valid image file.

        This method verifies if the file name ends with one of the 
        common image file extensions.

        Args:
            image_name (str): The name of the file to check.

        Returns:
            bool: True if the file is an image, False otherwise.
        """
        image_extensions: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.gif',
                                             '.bmp', '.tiff', '.webp')
        if not image_name.lower().endswith(image_extensions):
            return False
        return True


class DateUtil:
    """
    Utility class for converting date strings into datetime objects.

    This class contains methods and patterns for parsing date strings
    in various formats and converting them into datetime objects.
    Supported date formats include relative times (e.g., 'minutes ago'),
    specific date formats (e.g., 'Month day, year'), and standard date
    formats (e.g., 'month/day/4year'). It also handles empty date 
    strings.
    """

    __date_patterns = {
        # Matches dates like '1 minute ago' or '2 minutes ago'
        'minutes ago': r'(\d+) minute(s)? ago',
        # Matches dates like '1 hour ago' or '2 hours ago'
        'hours ago': r'(\d+) hour(s)? ago',
        # Matches dates like 'January 1, 2022', 'Jan 1, 2022' or
        # 'Jan. 1, 2022'
        'Month day, year': ( 
            r'(\w{3})\w*.? (0?[1-9]|[12][0-9]|3[01]), ([0-9]{4})'
        ),
        # Matches dates like '12/01/2022' or '12/1/2022'
        'month/day/4year': (
            r'^(0?[1-9]|1[0-2])\/(0?[1-9]|[12][0-9]|3[01])\/([0-9]{4})$'
        ),
        # Matches empty strings
        'empty': (
            r''
        )
    }

    @classmethod
    def date_to_datetime(cls, date: str) -> Optional[datetime]:
        """
        Converts a date string to a datetime object based on various 
        date formats.

        This method tries to match the provided date string against a 
        set of predefined date patterns. If a match is found, it 
        converts the string to a datetime object. The supported date 
        formats include relative time strings (e.g., 'minutes ago'),
        specific date formats (e.g., 'Month day, year'), and standard 
        date formats (e.g., 'month/day/4year').

        Args:
            date (str): The date string to be converted.

        Returns:
            Optional[datetime]: A datetime object if the conversion 
                                is successful, otherwise None.
        """
        for date_format, pattern in cls.__date_patterns.items():
            match: Optional[re.Match] = re.search(pattern, date)
            if match:
                if date_format == 'minutes ago':
                    minutes: int = int(match.group(1))
                    return datetime.now() - timedelta(minutes=minutes)
                elif date_format == 'hours ago':
                    hours: int = int(match.group(1))
                    return datetime.now() - timedelta(hours=hours)
                elif date_format == 'Month day, year':
                    month: int = match.group(1)
                    day: int = match.group(2)
                    year: int = match.group(3)
                    string_date: str = f'{month} {day}, {year}'
                    return datetime.strptime(string_date, '%b %d, %Y')
                elif date_format == 'month/day/4year':
                    return datetime.strptime(date, '%m/%d/%Y')
                elif date_format == 'empty':
                    warning_message: str = (
                        'The date string that is trying to be converted to '
                        'datetime is an empty string.'
                        )
                    logger.warning(warning_message)
                    return None
