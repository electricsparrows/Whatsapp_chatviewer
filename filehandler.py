import re
import sqlite3
from datetime import datetime, date, time
from dataclasses import dataclass
import db
from typing import List


def get_filepath():
    """ should connect to the gui """
    path = input("Please enter filepath: >>> ")
    return path



def loadfile(path: str):
    with open(path, encoding="utf-8") as f:
        # retrieve database connection
        conn = db.get_db()
        # generate a unique import reference
        import_ref = db.generate_import_ref(conn)
        msg_tups = []
        errs = []
        for line in f:
            try:
                tup = (import_ref, ) + parse(line)
                msg_tups.append(tup)
            except:
                errs.append(line)

        db.insert_parsed(conn, msg_tups)
        return f"success: {len(msg_tups)},\nmissed: {errs}"


def parse(line: str) -> tuple:
    """
    Decomposes a message record into component objects - datetime, speaker name, msg content
    Returns a tuple
    """
    metadata = line[:line.find(":", 20)]

    # parse the datetime stamp:
    msg_date = get_date(metadata)       # --> dt.date object
    msg_time = get_time(metadata)       # --> dt.time object
    msg_datetime = datetime.combine(msg_date, msg_time)

    # speaker name
    msg_speaker = metadata[metadata.find("-") + 2:]

    # message contents
    msg_body = line[line.find(":", 15) + 2:]
    # assess whether it is likely to be a conversation head

    # store decomposed info in a tuple.
    msg = (msg_datetime, msg_speaker, msg_body)

    return msg



def get_load_time(loadfunc, filepath):
    """For performance testing"""
    start = time.perf_counter()
    loadfunc(filepath)
    end = time.perf_counter()
    res = end - start
    print(f"performance: {res}s")


@dataclass(frozen=True)
class Message:
    msg_date: datetime
    msg_speaker: str
    msg_body: str


@dataclass
class Conversation:
    msgs: List[Message]


def get_date(s: str):
    """
    Takes a string and looks for any dates --> returns a datetime.date object
    Raises an exception if no date is found
    :param s: string with a date to be parsed.
    :return: a datetime.date object (Y, M, D)
    """
    (form, match) = get_date_match(s)

    forms = {"dmy": ["%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y"],
             "mdy": ["%m/%d/%Y", "%m/%d/%y", "%m-%d-%Y", "%m-%d-%y"]}
    try:
        it = iter(forms.get(form))
    except (AttributeError, TypeError):
        # No matching date format found in s
        return None

    while True:
        try:
            try:
                dt = datetime.strptime(match.group(), next(it)).date()
                return dt
            except ValueError:
                # tries again with next(it)
                continue
        except StopIteration:
            raise Exception("no date found")


def get_time(s: str):
    """
    Finds a time reference in given string s. Returns None if no reference is found.
    :param s: given string
    :return:  datetime.time object
    """
    try:
        match = get_time_match(s)
        t = datetime.strptime(match.group(), "%H:%M").time()
        return t
    except (AttributeError, TypeError):
        return None


def get_date_match(s: str):
    """
    Finds a date reference in given string by matching regex patterns
    Returns a two-tuple -- (string indicating date format ("dmy", "mdy"), match object)
    if there is no match, (None, None) is a returned.
    :param s: string data
    :return:  ("dmy" | "mdy", match object)
    """
    patterns = dict(dmy=r'\d{2}[-/]\d{2}[-/]\d{2}(\d\d)?', mdy=r'\d\d?[-/]\d\d?[-/]\d{2}(\d\d)?')
    (key, match) = (None, None)

    for reg in patterns.keys():
        key = reg
        match = re.search(patterns.get(key), s)
        if match is not None:
            break
        else:
            key = None
    return (key, match)


def get_time_match(s: str):
    """
    Finds a time reference in given string using regex
    Returns a single match object - if no match, returns None
    :param s: string data
    :return:  match object/ None
    """
    reg = r'([012]\d:[012345]\d)'
    match = re.search(reg, s)
    return match




