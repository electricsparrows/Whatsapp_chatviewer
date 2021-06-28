import re
from datetime import datetime, date, time


def parse(text: str):
    total = 0
    missed = 0
    msgs = []
    for s in text:
        try:
            metadata = s[:s.find(":", 15)]
            msg_date = get_date(metadata)       # --> date object
            msg_time = get_time_match(metadata) # --> time object
            dt = datetime.combine(msg_date, msg_time)

            msg_sender = metadata[metadata.find("-") + 2:]
            msg_body = s[s.find(":", 15) + 2:]
            # msg = Message(msg_date, msg_time, msg_sender, msg_body)
            msg = [msg_date, msg_time, msg_sender, msg_body]
            msgs.append(msg)
        except:
            missed += 1
            # print(f"line no. {total}, raw line: {s}")
            pass
        total += 1

    print(f"Total messages: {total}; missed: {missed}")
    return msgs


def get_date(s : str):
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
                pass
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


def get_date_match(s : str):
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


def get_time_match(s : str):
    """
    Finds a time reference in given string using regex
    Returns a single match object - if no match, returns None
    :param s: string data
    :return:  match object/ None
    """
    reg = r'([012]\d:[012345]\d)'
    match = re.search(reg, s)
    return match


# THE CODE DUMPSTER



