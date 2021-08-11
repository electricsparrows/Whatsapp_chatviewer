import time
from filehandler import parse
from dateutils import Date
from typing import List
from db import get_db, msg_wrapper, get_first_message, get_last_message, get_msgs_at_date, get_yoy_activity


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

'''# these can be removed with f strings
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
    '''


def get_messages_from_date_to_date(date1: Date, date2: Date, msgs: list) -> list:
    # just need to compute all dates between range date1, date2
    res = []
    current_date = date1
    while current_date < date2:
        try:
            res += get_msgs_at_date(str(current_date), msgs)
            current_date.increment()
        except:
            print(f"date {current_date} not found")
    return res

# Controller


def view_stats():
    print("viewing stats")
    conn = get_db()
    # retrieve first message in DB
    first_msg = msg_wrapper(get_first_message(conn))
    # retrieve last message in DB
    last_msg = msg_wrapper(get_last_message(conn))


def view_calendar():
    print("activity calendar view")
    conn = get_db()
    lt = get_yoy_activity(conn)
    # return dict {year : List[(date, #. of msgs for that date)}


def view_msgs_at_date():
    date_str = str(input("Enter a date (YYYY-MM-DD): >>> "))
    # input validation (pass from 'view module'
    # query DB -> List[msg_tups]
    conn = get_db()
    lt = get_msgs_at_date(conn, date_str)
    for mtup in lt:
        msg = msg_wrapper(mtup)
        # pass to GUI to render
    # print nav commands


def view_from_beginning():
    conn = get_db()
    first_msg = msg_wrapper(get_first_message(conn))
    print("first message")
    # render msg (in GUI)
    # load commands:
    # nav = {'a' : "prev day", 'd' : "next_day",
    #         "m" : "main_menu"}
    # print(nav)
    # nav_cmd = str(input("Pls enter a command: >>> "))


def search_by_keyword():
    query = input("Please enter a keyword: >>> ")
    # query string validation
    # query DB
    # render results
    print("we found nothing :D")


def main_menu():
    nav_menu = {
        "s": view_stats,
        "c": view_calendar,
        "d": view_msgs_at_date,
        "f": view_from_beginning,
        "r": search_by_keyword
    }

    running = True
    while running:
        print("Main menu:\n" +

              "- summary stats       (s)\n" +
              "- calendar view       (c)\n" +
              "- retrieve by date    (d)\n" +
              "- view from beginning (f)\n" +
              "- search messages     (r)")

        command = input("Enter a command: >>> ")
        command = str(command).strip()
        try:
            nav_menu[command]()

            while True:
                next_command = input("\n-- go back (b) or exit (exit)? >>> ")
                if next_command == 'b':
                    break
                elif next_command == "exit":
                    running = False
                    break
        except:
            if command == "exit":
                running = False
            else:
                print("no such command")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # print("Load a file (Y/n):")

    # file = loadfile("test02.txt")
    # msgs = parse(file)
    # print("---------------------------------")

    # Main menu
    main_menu()