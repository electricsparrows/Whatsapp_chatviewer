from datetime import datetime as dt
from pathlib import Path
import db
import filehandler as fh

# globals
test_files_dir = "C:\\Users\\Cindy\\PycharmProjects\\ChatViewer-testfiles"
p = Path(test_files_dir)

in_file = p / "test02.txt"
out_file = Path.cwd() / "out" / "output.xlsx"


def conversation_categorizer(data):
    """
    :param data: data should be messages with same date, import_ref (indicating imported from the same file,
    therefore the same chat thread), and should have a consistent group of participants. It is assumed that
    message records are sorted in chronological order and in order by msg_id (indexed).
    :return:
    """
    greetings = ["hi", "hey"]
    timegap_threshold = "01:00" # 1 hr
    split_ptrs= []

    # it is assumed that the given messages all both to one or more a conversations.

    # for each message in data
    # fetch msg_content -- change to all lower case.
    # if msg_content contains any greetings [‘\bHi\b’, ‘\bhello\b’ ]:
    #   --> reduce time-gap threshold to 30 mins.
    # elif: time-delta from prev message (by msg_id) > timegap_threshold.


def has_greetings(msg_content: str):
    words = msg_content


def calc_timedelta(time1: str, time2: str):
    # convert time strings to datetime objs
    dt1 = dt.strptime(time1, "%Y-%m-%d %H:%M:%S")
    pass


def main():
    s1 = "ok, more clear picture now"
    s2 = "i'll try to figure out what happens in ur body?"
    s3 = "Hi. How are you today?"
    has_greetings(s1)
    has_greetings(s2)
    has_greetings(s3)


if __name__ == '__main__':
    main()
