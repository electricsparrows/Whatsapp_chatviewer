import pytest
from datetime import datetime, date, time
from filehandler import *
from pathlib import Path


def get_args(pat):
    return RGX_PATTERNS[pat], DT_FORMATS[pat]


def get_lines1():
    return ["3/22/16, 13:41 - Mom: so u've determined to cut off all haribos and marshmallows",
            "3/22/16, 14:46 - Cindy L: 😑 I've determined to cut off sugar.",
            "3/22/16, 14:46 - Cindy L: Unfortunately everything has sugar",
            "3/22/16, 14:46 - Cindy L: So I'm terrified of eating anything now.",
            "3/22/16, 14:47 - Mom: cut off added sugar wud be good enough",
            "3/22/16, 14:47 - Mom: eat asian food with spice and salt",
            "3/22/16, 14:48 - Mom: wud that be better?",
            "3/22/16, 14:48 - Cindy L: No",
            "3/22/16, 14:48 - Cindy L: Rice has sugar.",
            "3/22/16, 14:48 - Cindy L: I don't know",
            "3/22/16, 14:48 - Cindy L: I stopped drinking juice for sure"]


def get_lines2():
    test_files_dir = "C:\\Users\\Cindy\\PycharmProjects\\ChatViewer-testfiles"
    p = Path(test_files_dir)
    in_file = p / "test01.txt"
    with open(in_file, mode='r', encoding='utf-8') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        return lines


def test_parse1():
    imp_ref = 2
    msg_tuples, err = parse(get_lines1(), imp_ref)
    print(msg_tuples)
    print(err)


def test_line_parse1():
    # normal pass case
    s = "21/09/2016, 01:16 - Alice: Just joking"
    rgx = r'[0123]\d/[01]\d/[12]\d{3}, [012]\d:[012345]\d -'
    fmt = "%d/%m/%Y, %I:%M -"
    tup = line_parse(s, rgx, fmt)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2016-09-21 01:16:00"
    assert tup[1] == "Alice"
    assert tup[2] == "Just joking"


def test_line_parse2():
    # normal pass case
    s = "11/20/15, 13:40 - Charlie M.: I got it in my Dropbox though"
    pat = 'pat3'
    rgx, fmt = get_args(pat)
    tup = line_parse(s, rgx, fmt)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2015-11-20 13:40:00"
    assert tup[1] == "Charlie M."
    assert tup[2] == "I got it in my Dropbox though"


def test_line_parse3():
    # normal pass case - content string has a \n character it in
    s = "23/07/2016, 03:34 - +44 7400 999333: disappointed that the Coco pops\n taste different here..."
    pat = 'pat2'
    rgx, fmt = get_args(pat)
    tup = line_parse(s, rgx, fmt)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2016-07-23 03:34:00"
    assert tup[1] == "+44 7400 999333"
    assert tup[2] == "disappointed that the Coco pops\n taste different here..."


def test_line_parse4():
    # timestamp  v1
    s = "11/20/15, 12:45 - Em: i send to ur email"
    pat = 'pat3'
    rgx, fmt = get_args(pat)
    tup = line_parse(s, rgx, fmt)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2015-11-20 12:45:00"
    assert tup[1] == "Em"
    assert tup[2] == "i send to ur email"


def test_line_parse5():
    # timestamp v2
    s = "23/09/2016, 08:23 - NAKAHARA: Yah I dunno why"
    pat = 'pat2'
    rgx, fmt = get_args(pat)
    tup = line_parse(s, rgx, fmt)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2016-09-23 08:23:00"
    assert tup[1] == "NAKAHARA"
    assert tup[2] == "Yah I dunno why"


def test_line_parse6():
    # timestamp v3.1
    s = "[12/3/2021, 3:29:04 PM] Christine M.: slept last night sitting up with head rested on edge of high table"
    pat = 'pat1'
    rgx, fmt = get_args(pat)
    tup = line_parse(s, rgx, fmt)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2021-03-12 15:29:04"
    assert tup[1] == "Christine M."
    assert tup[2] == "slept last night sitting up with head rested on edge of high table"


def test_line_parse7():
    """timestamp v3.2"""
    s = "[8/3/2021, 11:11:06 AM] +7758 123456: Notes to self"
    pat = 'pat1'
    rgx, fmt = get_args(pat)
    tup = line_parse(s, rgx, fmt)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2021-03-08 11:11:06"
    assert tup[1] == "+7758 123456"
    assert tup[2] == "Notes to self"


exception_cases = (
    "- Mandy: so how many pieces have u got by now?",
    "11/20/15, 12:40 - Mom:",
    '04/05/2016, 02:07 - You created group “Symptoms log”',
    '20/09/2016, 18:49 - Messages you send to this group...'
)


@pytest.mark.parametrize('s', exception_cases)
def test_line_parse_exceptions(s):
    """test cases with missing info should raise exception"""
    with pytest.raises(Exception):
        t = parse(s)


# get_name tests
# testcases = normal name, name with weird characters, phone number, no name

# get_content_str tests
# testcases = short message, long message, strange characters, hyperlinks


def test_guess_pattern_from_sample01():
    arg = ['11/20/15, 12:40 - Bob',
           '1/5/16, 03:14 - apple:',
           '2/20/16, 12:40 - Bob',
           '12/1/16, 12:40 - Bob',
           '11/25/15, 12:40 - Bob']
    foo = guess_pattern_from_sample(arg)
    assert foo == 'pat3'


def test_guess_pattern_from_sample02():
    arg = ['[4/10/2020, 2:20:56 PM] +44 7555 998877',
           '[4/11/2020, 2:20:56 PM] +44 7555 998877',
           '[23/10/2020, 2:20:56 PM] +44 7555 998877',
           '[2/2/2021, 8:01:59 PM] +44 7555 998877',
           '[13/4/2021, 7:25:08 PM] +44 7555 998877']
    foo = guess_pattern_from_sample(arg)
    assert foo == 'pat1'


def test_guess_pattern_from_sample03():
    arg = ['20/09/2016, 21:39 - Charles:',
           '11/10/2016, 04:58 - Rachel:',
           '13/10/2016, 12:55 - Charles:',
           '05/11/2016, 09:09 - Charles:',
           '12/11/2016, 06:53 - Rachel']
    foo = guess_pattern_from_sample(arg)
    assert foo == 'pat2'


def test_guess_pattern_from_sample04():
    arg = []
    with pytest.raises(Exception):
        guess_pattern_from_sample(arg)


# get_ts_ref
# test on testfiles
