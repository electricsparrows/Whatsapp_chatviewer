import datetime

import db
from controller import view_stats
from filehandler import parse, loadfile
from dateutils import Date
from db import get_db, msg_wrapper, get_first_message, get_last_message, get_msgs_at_date, get_yoy_activity

# String handling functions


def validate_datestr(str : str) -> bool:
    # is within universe of dates current to database atm
    try:
        # TODO check this-- check string is in ISO-8601 format
        datetime.datetime.strptime(str, "%Y-%m-%d")
        return True
    except:
        print("Please enter date in format YYYY-MM-DD")
        return False

def validate_tagstring(str: str) -> str:
    """
    checks given string starts with '#' and returns str in uniform casing.
    :param str:
    :return:
    """
    if str[0] == '#':
        return str.lower().strip()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    #input("Load a file (Y/n):>>> ")
    #file = loadfile("test02.txt")
    # print("---------------------------------")
    conn = db.get_db()
    import_ref = db.generate_import_ref()
    print(import_ref)