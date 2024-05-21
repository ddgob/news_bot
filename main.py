import argparse
from news_bot import LATimesScraper, config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LATimesScraper Command Line Arguments")
    parser.add_argument('-s', '--search_phrase', type=str, required=True, help='Search phrase')
    parser.add_argument('-e', '--excel_dir', type=str, required=True, help='Directory for Excel files')
    parser.add_argument('-i', '--image_dir', type=str, required=True, help='Directory for article images')
    parser.add_argument('-l', '--log_dir', type=str, required=True, help='Directory for log files')
    parser.add_argument('-sd', '--start_date', type=str, required=True, help='Start date (MM/DD/YYYY)')
    parser.add_argument('-ed', '--end_date', type=str, required=True, help='End date (MM/DD/YYYY)')
    args = parser.parse_args()
    config.LOG_FILE_DIR = args.log_dir
    scraper = LATimesScraper(
        phrase=args.search_phrase, 
        excel_files_dir=args.excel_dir, 
        article_images_dir=args.image_dir, 
        start_date=args.start_date, 
        end_date=args.end_date
    )
    scraper.run()