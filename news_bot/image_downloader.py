from RPA.HTTP import HTTP
from .logger import Logger
from .articles.article_list import ArticleList

class ImageDownloader:
    def __init__(self) -> None:
        self.__log = Logger().log
        self.__http: HTTP = HTTP()

    def download_image(self, image_url: str, image_path: str) -> None:
        try:
            self.__log('info', f'Downloading image from {image_url}...')
            self.__http.download(image_url, image_path)
            self.__log('info', f'Finished downloading image from {image_url}')
        except Exception as e:
            error_message: str = (
                f'An error occurred while downloading image from {image_url}: '
                f'{e}'
            )
            self.__log('error', error_message)

    def download_images(self, articles: ArticleList, images_dir: str) -> None:
        for article in articles:
            image_url: str = article.get_image_url()
            image_name: str = article.get_image_file_name()
            image_path: str = f'{images_dir}/{image_name}'
            self.download_image(image_url, image_path)