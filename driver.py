import time
from filehandler import parse
from dateutils import Date


def loadfile(path):
    with open(path, encoding="utf-8") as f:
        ftext = []
        for line in f.readlines():
            ftext.append(line)
        return ftext


def get_load_time():
    """For performance testing"""
    start = time.perf_counter()
    loadfile("test02.txt")
    end = time.perf_counter()
    res = end - start
    print(f"performance: {res}s")


# TODO
def get_messages_at_date(date: Date, msgs: list):
    """
    :param date: string representing a date in format YYYY-MM-DD
    :param msgs: set of msg objects (list for now, connect to database later)
    :return:
    """
    date_str = str(date.get_date())
    yyyy = date_str[0:4]
    mm = date_str[5:7]
    dd = date_str[8:10]
    query = f"{mm}/{dd}/{yyyy}"  # haha this is bad
    return [m for m in msgs if str(m.get_date()) == query]


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


def get_messages_from_date_to_date(date1: Date, date2: Date, msgs: list) -> list:
    """
    Returns a list of message objects dated between date1 and date2 (exclusive)
    :param date1: start date range
    :param date2: end date range (exclusive)
    :param msgs: list of message objects (TODO: retrieved from database)
    :return: filtered list of messages
    """
    res = []
    current_date = date1
    while current_date < date2:
        try:
            res += get_messages_at_date(current_date, msgs)
            current_date.increment()
        except:
            print(f"date {current_date} not found")
    return res


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("load a file")
    rawtext = loadfile("test02.txt")
    msgs = parse(rawtext)
    print("---------------------------------")
    print("Main menu:\n" +
          "- summary stats + calendar view\n" +
          "- view from beginning" +
          "- view by date")
