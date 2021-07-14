# This module works with dates
from datetime import datetime

def indexDates(msgs: list):  # this needs to be a singleton
    index = {}  # <String date, int index>
    current_date = ""
    for i in range(len(msgs)):
        if msgs[i] != current_date:
            current_date = msgs[i][0]
            if current_date not in index:
                index[current_date] = i
    return index


class DateOps:
    # TODO extend datetime
    def __init__(self, dt):
        __date = dt.date()
        self.DAY = __date.DAY
        self.MONTH = __date.MONTH
        self.YEAR = __date.YEAR

    def get_days_in_months(self):
        return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def increment(self):
        # TODO rewrite to update the __date object
        dates = self.get_days_in_months()
        if self.DAY > dates[self.MONTH - 1]:
            self.DAY = 1
            if self.MONTH + 1 > 12:
                self.YEAR += 1
                self.MONTH = 1
            else:
                self.MONTH += 1

    def get_next_day(self) -> datetime:
        dates = self.get_days_in_months()
        d = self.DAY + 1
        m = self.MONTH
        y = self.YEAR
        if d > dates[self.MONTH - 1]:
            d = 1
            if self.MONTH + 1 > 12:
                y = self.YEAR + 1
                m = 1
            else:
                m = self.MONTH + 1
        return datetime(y, m, d)

    # get prev date
    # decrement

    def __str__(self):
        return f"{self.DAY}/{self.MONTH}/{self.YEAR}"


    # these functions belong with message class, need to be renamed -- TODO
    def __eq__(self, other):
        if isinstance(other, Message):
            return self.DATE == other.DATE and self.MONTH == other.MONTH and self.YEAR == other.YEAR
        else:
            return False

    # earlier dates are less than later dates and vice versa
    def __lt__(self, other):
        if self == other:
            return False
        if self.YEAR == other.YEAR:
            if self.MONTH == other.MONTH:
                return self.DAY < other.DAY
            else:
                return self.MONTH < other.MONTH
        else:
            return self.YEAR < other.YEAR

    def __gt__(self, other):
        if self == other:
            return False
        if self.YEAR == other.YEAR:
            if self.MONTH == other.MONTH:
                return self.DAY > other.DAY
            else:
                return self.MONTH > other.MONTH
        else:
            return self.YEAR > other.YEAR