from urllib.parse import urlparse, parse_qs
from typing import Any

from .logger import Logger


class URLHandler:
    """
    Handles URL parsing and extraction tasks.
    """

    def __init__(self) -> None:
        """
        Initialize the URLHandler.

        Sets up the logger for logging activities.
        """
        self.__log = Logger().log

    def get_image_url(cls, image_src) -> str:
        """
        Extract the image URL from a given image source URL.

        Args:
            image_src (str): The source URL containing the image URL as 
            a query parameter.

        Returns:
            str: The extracted image URL.

        Raises:
            ValueError: If the image URL cannot be extracted from the 
            source URL.
        """
        parsed_url: Any = urlparse(image_src)
        query_params: Any = parse_qs(parsed_url.query)
        image_url: Any = query_params.get('url', [None])[0]
        if image_url is None:
            error_message: str = (
                f'An error occurred while getting image url: the url returned '
                f'None for image source image_src {image_src}'
            )
            cls.__log('error', error_message)
            raise ValueError(error_message)
        return image_url