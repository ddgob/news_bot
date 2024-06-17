"""
This script uses the LATimesNewsBot to scrape articles from the LA 
Times website.

The script retrieves input parameters (phrase, topic, number_of_months) 
from work items, initializes the news bot, and scrapes articles based 
on the given parameters. The results are saved to an Excel file and 
images are downloaded to the specified artifacts directory.

Dependencies:
    - datetime
    - calendar
    - dateutil.relativedelta
    - RPA.Robocorp.WorkItems
    - news_bot.LATimesNewsBot

Usage:
    The script is designed to be run as a standalone program.
    It retrieves work item variables and uses them to perform the 
    scraping.
"""

from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta

from RPA.Robocorp.WorkItems import WorkItems

from news_bot import LATimesNewsBot

def month_start_end_dates(months_count: int) -> tuple[datetime, datetime]:
    """
    Calculate the start and end dates for a given number of months
      before the current date.

    Args:
        number_of_months (int): The number of months before the current 
                                date.

    Returns:
        tuple: A tuple containing the start and end dates for the given 
               month range.
    """
    now_date: datetime = datetime.now()
    # Get the last day of the current month
    last_day_of_month: int = calendar.monthrange(now_date.year,
                                                 now_date.month)[1]
    end: datetime = datetime(now_date.year, now_date.month,
                                  last_day_of_month, hour=23, minute=59,
                                  second=59)
    # Calculate the start date based on the number of months
    if months_count >= 2:
        months_before = relativedelta(months=months_count - 1)
    else:
        months_before = relativedelta(months=0)
    year: int = (now_date - months_before).year
    month: int = (now_date - months_before).month
    start: datetime = datetime(year, month, day=1)

    return start, end

if __name__ == '__main__':
    # Get input work item variables
    work_items: WorkItems = WorkItems()
    work_items.get_input_work_item()
    phrase: str = work_items.get_work_item_variable('phrase')
    topic: str = work_items.get_work_item_variable('topic')
    number_of_months: int = work_items.get_work_item_variable('number_of_months')
    # Get additional news bot parameters
    start_date, end_date = month_start_end_dates(number_of_months)
    ARTIFACTS_DIR: str = 'output'
    excel_dir: str = f"{ARTIFACTS_DIR}/{datetime.now().strftime('%m-%d-%Y_%H-%M')}.xlsx"
    IMAGES_DIR: str = ARTIFACTS_DIR
    # Initialize and run the news bot
    news_bot: LATimesNewsBot = LATimesNewsBot(excel_dir, IMAGES_DIR)
    news_bot.run(phrase, start_date, end_date, topic)
