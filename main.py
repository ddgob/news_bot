import argparse
from news_bot import NewsBot, config

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
    news_bot = NewsBot()
    news_bot.scrape_articles_by_date_range('https://www.latimes.com/', 
                                           args.search_phrase, args.start_date, 
                                           args.end_date, args.excel_dir, 
                                           args.image_dir
                                           )