from datetime import datetime, timedelta
import re

from .logger import Logger


class DateHandler:
    """
    Handles date conversion and manipulation tasks.
    """

    __date_regex_patterns = {
        'minutes ago': r'(\d+) minute(s)? ago',
        'hours ago': r'(\d+) hour(s)? ago',
        'Short month day, year': (
            r'(\w{3}).? (0?[1-9]|[12][0-9]|3[01]), ([0-9]{4})'
        ),
        'month/day/4year': (
            r'^(0?[1-9]|1[0-2])\/(0?[1-9]|[12][0-9]|3[01])\/([0-9]{4})$'
        )
    }

    def __init__(self) -> None:
        """
        Initialize the DateHandler.

        Sets up the logger for logging activities.
        """
        self.__log = Logger().log

    def __get_string_date_format(self, unconverted_date: str):
        """
        Identify the format of a date string.

        Args:
            unconverted_date (str): The date string to identify.

        Returns:
            tuple: A tuple containing the identified format and the 
            match object.

        Raises:
            ValueError: If the date format is not recognized.
        """
        if minutes_match := re.search(
            self.__date_regex_patterns['minutes ago'], unconverted_date
            ):
            return 'minutes ago', minutes_match
        elif hours_match := re.search(
            self.__date_regex_patterns['hours ago'], unconverted_date
            ):
            return 'hours ago', hours_match
        elif short_month_day_year_match := re.search(
            self.__date_regex_patterns['Short month day, year'], 
            unconverted_date
            ):
            return 'Short month day, year', short_month_day_year_match
        elif month_day_year_match := re.search(
            self.__date_regex_patterns['month/day/4year'], unconverted_date
            ):
            return 'month/day/4year', month_day_year_match
        else:
            error_message = (
                f'Was not able to recognize date format of date '
                f'{unconverted_date} '
            )
            self.__log('error', error_message)
            raise ValueError(error_message)

    def convert_date_to_datetime(self, unconverted_date: str):
        """
        Convert a date string to a datetime object.

        Args:
            unconverted_date (str): The date string to convert.

        Returns:
            datetime: The converted datetime object.

        Raises:
            ValueError: If the date format is not recognized or cannot 
            be converted.
        """
        date_format, date_match = self.__get_string_date_format(
            unconverted_date
            )
        if date_format == 'minutes ago':
            minutes = int(date_match.group(1))
            return datetime.now() - timedelta(minutes=minutes)
        elif date_format == 'hours ago':
            hours = int(date_match.group(1))
            return datetime.now() - timedelta(hours=hours)
        elif date_format == 'Short month day, year':
            short_month = date_match.group(1)
            day = date_match.group(2)
            year = date_match.group(3)
            date_string = f'{short_month} {day}, {year}'
            return datetime.strptime(date_string, '%b %d, %Y')
        elif date_format == 'month/day/4year':
            month = date_match.group(1)
            day = date_match.group(2)
            year = date_match.group(3)
            date_string = f'{month}/{day}/{year}'
            return datetime.strptime(unconverted_date, '%m/%d/%Y')
        else:
            error_message = (
                f'Was not able to convert date {unconverted_date} that has '
                f'format {date_format}'
            )
            self.__log('error', error_message)
            raise ValueError(error_message)
    
    def convert_datetime_to_string(self, date_obj: datetime, 
                                   separator=None, is_show_time=False) -> str:
        """
        Convert a datetime object to a formatted date string.

        Args:
            date_obj (datetime): The datetime object to convert.
            separator (str, optional): The separator to use in the date 
                                       string. Defaults to None.
            is_show_time (bool, optional): Whether to include time in 
                                           the string. Defaults to False.

        Returns:
            str: The formatted date string.
        """
        format_string = ''
        if is_show_time:
            if separator == None:
                format_string = '%m/%d/%Y_%H-%M-%S'
            elif separator == '-':
                format_string = '%m-%d-%Y_%H-%M-%S'
        else:
            if separator == None:
                format_string = '%m/%d/%Y'
            elif separator == '-':
                format_string = '%m-%d-%Y'
        return date_obj.strftime(format_string)
    
    def first_date_earlier_than_second(self, first_date: str, 
                                       second_date: str):
        """
        Ensure the first date is earlier than the second date.

        Args:
            first_date (str): The first date string.
            second_date (str): The second date string.

        Returns:
            tuple: A tuple containing the two dates in chronological 
            order.
        """
        first_date = self.convert_date_to_datetime(first_date)
        second_date = self.convert_date_to_datetime(second_date)
        if second_date < first_date:
            first_date, second_date = second_date, first_date
        return first_date, second_date

    
    def make_until_end_of_day(self, date: datetime):
        """
        Extend the given date to the end of the day.

        Args:
            date (datetime): The date to extend.

        Returns:
            datetime: The date extended to the end of the day.
        """
        date += timedelta(hours=23, minutes=59, seconds=59, milliseconds=59)
        return date