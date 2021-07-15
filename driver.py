from datetime import datetime
import time
from parser import parse


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
