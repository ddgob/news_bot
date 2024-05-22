from .logger import Logger
from datetime import datetime, timedelta
import re
from typing import Any


class DateHandler:
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
        self.__log = Logger().log

    def __get_string_date_format(self, unconverted_date: str):
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