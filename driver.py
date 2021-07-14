from datetime import datetime
import time
from Parser import parse


def loadfile(path):
    with open(path, encoding="utf-8") as f:
        ftext = []
        for line in f.readlines():
            ftext.append(line)
        return ftext


def get_load_time():
    start = time.perf_counter()
    loadfile("test02.txt")
    end = time.perf_counter()
    res = end - start
    print("performance: " + str(res) + "s")





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

    # these functions are redundant with datetime -- TODO delete
    def __str__(self):
        return f"{self.DAY}/{self.MONTH}/{self.YEAR}"

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


def indexDates(msgs: list):  # this needs to be a singleton
    index = {}  # <String date, int index>
    current_date = ""
    for i in range(len(msgs)):
        if msgs[i] != current_date:
            current_date = msgs[i][0]
            if current_date not in index:
                index[current_date] = i
    return index


# TODO update getMessagesAtDate to use datetime -- this thing needs to be rewritten
def getMessagesAtDate(date: str, msgs: list):
    mm = __datemonth_formatter(date.MONTH)
    dd = __datemonth_formatter(date.DAY)
    yyyy = __year_formatter(date.YEAR)
    query = f"{mm}/{dd}/{yyyy}"  # haha this is bad
    # index = indexDates(msgs)
    return [m for m in msgs if m[0] == query]


def __datemonth_formatter(n: int):
    """
    Takes date/month in int format --> returns its 2 digit string representation
    Raises a ValueError if input is not valid
    :param n:  date/ month as an integer in range [1-31]
    :return:   equivalent string representation of date/ month
    """
    numstr = str(n)
    if len(numstr) < 2:
        numstr = "0" + numstr
    elif len(numstr) > 2:
        raise ValueError
    return numstr


def __year_formatter(n: int):
    """
    Takes year in int format --> returns its full 4 digit string representation
    Raises a ValueError if input is not valid
    :param n:  year as an integer, possibly in compacted form
    :return:   equivalent string representation of year
    """
    numstr = str(n)
    while len(numstr) < 4:
        numstr = "0" + numstr
    if len(numstr) > 4:
        raise ValueError
    return numstr


# TODO refactor get_messages_from_date_to_date() to use datetime
def getMessagesFromDateToDate(date1: Date, date2: Date, msgs: list):
    res = []
    current_date = date1
    while current_date < date2:
        try:
            res += getMessagesAtDate(current_date, msgs)
            current_date.increment()
        except:
            print(f"date {current_date} not found")
    return res


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rawtext = loadfile("test02.txt")
    msgs = parse(rawtext)
    print("---------------------------------")
    lt = getMessagesFromDateToDate(Date(10, 6, 2016), Date(9, 6, 2016), msgs)

    for item in lt:
        print(item)
