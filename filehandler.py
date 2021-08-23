import re
import random as rdm
from datetime import datetime as dt
import db
from typing import List
import time


# module constants
RGX_PATTERNS = {
        'pat1': r'\[\d+/\d+/[12]\d{3}, [12]?\d:[012345]\d:[012345]\d [AP]M\]',  # "[d/m/YYYY, HH:MM:SS [AP]M]"
        'pat2': r'[0123]\d/[01]\d/[12]\d{3}, [012]\d:[012345]\d -',  # "dd/mm/YYYY, HH:MM -"
        'pat3': r'\d+/\d+/\d\d, [012]\d:[012345]\d -'  # "m/d/yy, HH:MM -"
    }

DT_FORMATS = {
    'pat1': "[%d/%m/%Y, %I:%M:%S %p]",
    'pat2': "%d/%m/%Y, %I:%M",
    'pat3': "%d/%m/%y, %I:%M",
}


def get_filepath():
    """ should connect to the gui """
    path = input("Please enter filepath: >>> ")
    return path


def loadfile(path: str):
    """
    This is the key function
    :param path:
    :return:
    """
    # open file and get lines:
    lines = open_file(path)

    # retrieve database connection
    conn = db.get_db()

    # generate a unique import reference
    import_ref = db.generate_import_ref(conn)

    # parse msg data tokens from lines
    msg_tuples, errs = parse(lines, import_ref)

    # insert into db
    db.insert_parsed(conn, msg_tuples)

    return f"success: {len(msg_tuples)},\nmissed: {errs}"


def open_file(path):
    """Opens file at given path and reads each line --> Returns list of strings"""
    with open(path, mode='r', encoding='utf-8') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        return lines


def parse(lines, import_ref):
    """
        Parse operations by lines
        :param lines: read lines in file
        :param ts_ref: reference to timestamp pattern used by file - obtained from ts_sampling
        :param import_ref: import reference
        :return: list of message tuples
    """
    ts_ref = get_ts_ref(lines)
    rgx = RGX_PATTERNS[ts_ref]
    fmt = DT_FORMATS[ts_ref]
    msg_tuples = []
    err = []
    for ln in lines:
        try:
            msg = (import_ref,) + line_parse(ln, rgx, fmt)
            msg_tuples.append(msg)
        except (AttributeError, ValueError):
            # line has no date/ unknown timestamp/ no name/ no content
            err.append(ln)
    return msg_tuples, err


def line_parse(ln: str, rgx, fmt) -> tuple:
    """
    retrieves tokenized strings for datetime, name, message content
    :param ln: line from file
    :param rgx: regex pattern matching date-time string
    :param fmt: date time format matching date-time string
    :return: decomposed info in a tuple - (datetime: datetime, speaker name: str, msg_content: str)
    """
    datetime_str = re.match(ln, rgx).group()
    k = len(datetime_str)

    msg_dt = dt.strptime(datetime_str, fmt)

    msg_name = get_name(ln, k)

    msg_content = get_content_str(ln, k)

    return (msg_dt, msg_name, msg_content)


def get_load_time(loadfunc, filepath):
    """For performance testing"""
    start = time.perf_counter()
    loadfunc(filepath)
    end = time.perf_counter()
    res = end - start
    print(f"performance: {res}s")


def get_name(ln, k):
    """
    Tokenizes name of speaker associated with message in given line.
    -  ValueError is raised if the metadata delimiter (:) cannot be found
    :param ln: line from file containing data for a message record
    :param k: length of the (datetime_str)
    :return: string containing speaker name; ValueError
    """
    if ln.find(':', k) == -1:
        raise ValueError("cannot locate metadata substring, name may not exist")
    else:
        msg_name = ln[k: ln.find(':', k)].strip()
        return msg_name.encode("ascii", "ignore").decode()


def get_content_str(ln:str, k:int):
    """
    Parses message content data from given line
    - ValueError is raised if the metadata delimiter (:) cannot be found
    :param ln: line from file containing data for a message record
    :param k: length of the (datetime_str)
    :return: string containing message content; ValueError
    """
    if ln.find(':', k) == -1:
        raise ValueError("cannot locate metadata substring, content may not exist")
    else:
        return ln[ln.find(':', k):].strip()


def get_ts_ref(lines):
    # collect random sample, examine the timestamps
    samp = sample_timestamps(lines)
    # decide which timestamp pattern is correct.
    return guess_pattern_from_sample(samp)


def sample_timestamps(lines):
    """returns a random sample of timestamp strings from imported records"""
    n = len(lines)
    sample = [rdm.randint(0, len(lines)) for x in range(10)]
    # get timestamps from those records.
    ts = []
    for i in range(n):
        if i in sample:
            ln = lines[i]
            metadata = ln[:ln.find(":", 15)]
            ts.append(metadata)
    return ts


def guess_pattern_from_sample(ts_sample: List[str]):
    """returns best guess of ts pattern for given sample timestamps"""
    patterns = RGX_PATTERNS
    tal = {}
    for s in ts_sample:
        for pat_ref, rgx in patterns.items():
            if re.match(rgx, s) is not None:
                if pat_ref in tal.keys():
                    tal[pat_ref] += 1
                else:
                    tal[pat_ref] = 1
    # get highest freq:
    mode = max(tal.values())
    for k, v in tal.items():
        if v == mode:
            return k





