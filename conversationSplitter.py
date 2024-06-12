import datetime
import string
from datetime import datetime as dt
from pathlib import Path
from typing import List

import db

# globals
test_files_dir = "C:\\Users\\Cindy\\PycharmProjects\\ChatViewer-testfiles"
p = Path(test_files_dir)

in_file = p / "test02.txt"
out_file = Path.cwd() / "out" / "output.xlsx"


def conversation_splitter(data : List[dict]):
    """
    :param data: data should be messages with same date, import_ref (indicating imported from the same file,
    therefore the same chat thread), and should have a consistent group of participants. It is assumed that
    message records are sorted in chronological order and in order by msg_id (indexed).

    - it is assumed that all messages belong to one or more conversations.
    :return: list of msg_id of messages classified as convo_heads
    """
    timegap_threshold = datetime.timedelta(seconds=3600)    # 1 hr gap between messages
    convo_heads = [data[0]['msg_id']]
    prev_dtstr  = None

    for m in data:
        # if msg_content contains any greeting, reduce time-gap threshold to 30 mins
        if has_greetings(m['msg_content']):
            timegap_threshold = datetime.timedelta(seconds=1800)

        if calc_timedelta(prev_dtstr, m['date_time']) > timegap_threshold:
            convo_heads.append(m['msg_id'])
        prev_dtstr = m['date_time']
    return convo_heads


def convert_dtstr_to_datetime(dt_str: str) -> datetime.datetime:
    return dt.strptime(dt_str, "%Y-%m-%d %H:%M:%S")


def has_greetings(msg_content: str) -> bool:
    greetings = ("hi", "hello", "hey", "yo", "hiya")
    words = [w.strip(string.punctuation) for w in msg_content.lower().split()]
    for g in greetings:
        if g in words:
            return True
    return False


def calc_timedelta(time1: str, time2: str) -> datetime.timedelta:
    """converts time strings to datetime objs; it is assumed that time2 is after time1 (t2 > t1)"""
    if time1 is None or time2 is None:
        return datetime.timedelta(seconds=0)
    dt1 = convert_dtstr_to_datetime(time1)
    dt2 = convert_dtstr_to_datetime(time2)
    return abs(dt2 - dt1)                   # timedelta in seconds


def main():
    data = db.get_msgs_at_date("2016-01-06")
    ptrs = conversation_splitter(data)
    for ch in ptrs:
        print(db.read_msg(ch)['msg_content'])


if __name__ == '__main__':
    main()
