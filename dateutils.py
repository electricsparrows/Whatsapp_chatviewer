from datetime import datetime

# This module works with dates

def indexDates(msgs: list):  # this needs to be a singleton
    index = {}  # <String date, int index>
    current_date = ""
    for i in range(len(msgs)):
        if msgs[i] != current_date:
            current_date = msgs[i][0]
            if current_date not in index:
                index[current_date] = i
    return index


class Date:
    def __init__(self, dt: datetime):
        self.__date = dt  # this is some datetime object

    @staticmethod
    def get_days_in_month(m: int, leap_year=False) -> int:
        """
        returns the number of days in given month m
        :param m: an integer indicating the month
        :param leap_year: default to False. If set to True, February returns 29 days
        """
        if m == 2 and leap_year is True:
            return 29

        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return days[m - 1]

    @staticmethod
    def is_leap_year(year: int) -> bool:
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def get_date(self):
        return self.__date

    def get_next_date(self) -> datetime:
        d = self.get_date().day + 1
        m = self.get_date().month
        y = self.get_date().year
        max_days_in_month = self.get_days_in_month(m, self.is_leap_year(y))

        if d > max_days_in_month:
            d = 1
            if m + 1 > 12:
                y += 1
                m = 1
            else:
                m += 1
        return datetime(y, m, d)

    def get_prev_date(self) -> datetime:
        d = self.get_date().day - 1
        m = self.get_date().month
        y = self.get_date().year
        if d < 1:
            if m - 1 < 1:
                y -= 1
                if y < 0:
                    raise ValueError("Year cannot be negative")
                else:
                    m = 12
            else:
                m -= 1
            d = self.get_days_in_month(m, self.is_leap_year(y))
        return datetime(y, m, d)

    def increment(self):
        """mutates the Date instance"""
        self.__date = self.get_next_date()

    def decrement(self):
        self.__date = self.get_prev_date()

    def __str__(self):
        return str(self.get_date().date())

    def __eq__(self, other_obj):
        if isinstance(other_obj, Date):
            return self.get_date() == other_obj.get_date()
        else:
            return False

    # earlier dates are less than later dates and vice versa
    def __lt__(self, other_obj):
        if self == other_obj:
            return False
        else:
            return self.get_date() < other_obj.get_date()

    def __gt__(self, other_obj):
        if self == other_obj:
            return False
        else:
            return self.get_date() > other_obj.get_date()
