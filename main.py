"""import argparse
from news_bot import NewsBot, config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="LATimesScraper Command Line Arguments"
        )
    parser.add_argument('-s', '--search_phrase', type=str, required=True, 
                        help='Search phrase'
                        )
    parser.add_argument('-e', '--excel_dir', type=str, required=True, 
                        help='Directory for Excel files'
                        )
    parser.add_argument('-i', '--image_dir', type=str, required=True, 
                        help='Directory for article images'
                        )
    parser.add_argument('-l', '--log_dir', type=str, required=True, 
                        help='Directory for log files'
                        )
    parser.add_argument('-sd', '--start_date', type=str, required=True, 
                        help='Start date (MM/DD/YYYY)'
                        )
    parser.add_argument('-ed', '--end_date', type=str, required=True, 
                        help='End date (MM/DD/YYYY)'
                        )
    args = parser.parse_args()
    config.LOG_FILE_DIR = args.log_dir
    news_bot = NewsBot()
    news_bot.scrape_articles_by_date_range('https://www.latimes.com/', 
                                           args.search_phrase, args.start_date, 
                                           args.end_date, args.excel_dir, 
                                           args.image_dir
                                           )"""





import argparse
import os
from datetime import datetime
from news_bot import NewsBot, config

def validate_date(date_str: str):
    try:
        is_valid: bool = True
        date: datetime = datetime.strptime(date_str, "%m/%d/%Y")
        return (date, is_valid)
    except ValueError:
        is_valid = False
        print(f"Invalid date format: '{date_str}'. Use MM/DD/YYYY.")
        return (None, is_valid)

def validate_directory(dir_str: str):
    if not os.path.isdir(dir_str) or dir_str == '':
        print(f"Directory does not exist: '{dir_str}'.")
        return None, False
    if not os.access(dir_str, os.W_OK):
        print(f"Directory is not writable: '{dir_str}'.")
        return None, False
    return (dir_str, True)

def prompt_for_invalid_args(args) -> None:
    if args.search_phrase is None:
        is_sure = False
        while not is_sure:
            args.search_phrase = input('Enter search phrase: ')
            sure_answer = input(f"Is '{args.search_phrase}' correct? (y/n): ")
            if sure_answer.lower() == 'y':
                is_sure = True
            else:
                print("Let's try again")
    if args.excel_dir is None or not args.excel_dir[1]:
        is_valid = False
        while not is_valid:
            args.excel_dir, is_valid = validate_directory(
                input('Enter directory where the Excel file should be '
                      'stored: ')
                )
    else:
        args.excel_dir = args.excel_dir[0]
    if args.image_dir is None or not args.image_dir[1]:
        is_valid = False
        while not is_valid:
            args.image_dir, is_valid = validate_directory(
                input('Enter directory where the article images should be '
                      'stored: ')
                )
    else:
        args.image_dir = args.image_dir[0]
    if args.log_dir is None or not args.log_dir[1]:
        is_valid = False
        while not is_valid:
            args.log_dir, is_valid = validate_directory(
                input('Enter directory where the log file for the program '
                      'execution should be stored: ')
                )
    else:
        args.log_dir = args.log_dir[0]
    if args.start_date is None or not args.start_date[1]:
        is_valid = False
        while not is_valid:
            args.start_date, is_valid = validate_date(
                input('Enter start date (MM/DD/YYYY): ')
                )
            if not is_valid:
                print(("Use a date in the format that the example 11/23/2024 "
                       "uses")
                       )
    else:
        args.start_date = args.start_date[0]
    if args.end_date is None or not args.end_date[1]:
        is_valid = False
        while not is_valid:
            args.end_date, is_valid = validate_date(
                input('Enter end date (MM/DD/YYYY): ')
                )
            if not is_valid:
                print(("Use a date in the format that the example 11/23/2024 "
                       "uses")
                       )
    else:
        args.end_date = args.end_date[0]

def main():
    parser = argparse.ArgumentParser(
        description="NewsBot Command Line Arguments"
        )
    parser.add_argument('-s', '--search_phrase', type=str, 
                        help='Search phrase'
                        )
    parser.add_argument('-e', '--excel_dir', type=validate_directory, 
                        help='Directory for Excel files'
                        )
    parser.add_argument('-i', '--image_dir', type=validate_directory, 
                        help='Directory for article images'
                        )
    parser.add_argument('-l', '--log_dir', type=validate_directory, 
                        help='Directory for log files'
                        )
    parser.add_argument('-sd', '--start_date', type=validate_date, 
                        help='Start date (MM/DD/YYYY)'
                        )
    parser.add_argument('-ed', '--end_date', type=validate_date, 
                        help='End date (MM/DD/YYYY)'
                        )
    args = parser.parse_args()

    prompt_for_invalid_args(args)

    config.LOG_FILE_DIR = args.log_dir
    news_bot = NewsBot()
    news_bot.scrape_articles_by_date_range(
        'https://www.latimes.com/', 
        args.search_phrase, 
        args.start_date.strftime("%m/%d/%Y"), 
        args.end_date.strftime("%m/%d/%Y"), 
        args.excel_dir, 
        args.image_dir
    )

if __name__ == '__main__':
    main()
