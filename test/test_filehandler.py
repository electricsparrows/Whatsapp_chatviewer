import pytest
from datetime import datetime, date, time
from filehandler import *


def test_parse1():
    # normal pass case
    tup = parse("21/09/2016, 01:16 - Alice: Just joking")
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2016-09-21 01:16:00"
    assert tup[1] == "Alice"
    assert tup[2] == "Just joking"

def test_parse2():
    # no speaker name found - raise exception
    with pytest.raises(Exception):
        tup = parse('04/05/2016, 02:07 - You created group “Symptoms log”')


def test_parse3():
    # no speaker name found - raise exception
    with pytest.raises(Exception):
        tup = parse('20/09/2016, 18:49 - Messages you send to this group...')

def test_parse4():
    # timestamp  v1
    s = "11/20/15, 12:45 - Em: i send to ur email"
    tup = parse(s)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2015-11-20 12:45:00"
    assert tup[1] == "Em"
    assert tup[2] == "i send to ur email"


def test_parse5():
    # timestamp v2
    s = "23/09/2016, 08:23 - NAKAHARA: Yah I dunno why"
    tup = parse(s)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2016-09-23 08:23:00"
    assert tup[1] == "NAKAHARA"
    assert tup[2] == "Yah I dunno why"


def test_parse6():
    # timestamp v3.1
    s = "[12/3/2021, 3:29:04 PM] Christine M.: slept last night sitting up with head rested on edge of high table"
    tup = parse(s)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2021-03-12 15:29:04"
    assert tup[1] == "Christine M."
    assert tup[2] == "slept last night sitting up with head rested on edge of high table"


def test_parse7():
    # timestamp v3.2
    s = "[8/3/2021, 11:11:06 AM] +7758 123456: Notes to self"
    tup = parse(s)
    assert isinstance(tup[0], datetime)
    assert str(tup[0]) == "2021-03-12 11:11:06"
    assert tup[1] == "+7758 123456"
    assert tup[2] == "Notes to self"


def test_get_date1():
    assert get_date("14/01/2019") == datetime(2019, 1, 14).date()


def test_get_date2():
    assert get_date("1/14/19") == datetime(2019, 1, 14).date()


def test_get_date3():
    assert get_date("02/10/2016, 19:40 - Person:") == datetime(2016, 10, 2).date()


def test_get_date4():
    assert get_date("1/15/16, 05:28") == datetime(2016, 1, 15).date()


def test_get_date5():
    assert get_date("aapples") is None


def test_get_date6():
    s = "[8/3/2021, 11:11:06 AM] You:"
    assert get_date(s) == datetime(2021, 3, 8).date()


def test_get_time_match1():
    assert get_time_match("12:30").group() == "12:30"


def test_get_time_match2():
    assert get_time_match("20L1239") is None


def test_get_time_match3():
    assert get_time_match("10-23-19, 15:21").group() == "15:21"


def test_get_time_match4():
    assert get_time_match("15:21 -- 10-23-19").group() == "15:21"


def test_get_time1():
    assert get_time("12:30") == time(12, 30)


def test_get_time2():
    assert get_time("29:83") is None
    # Should this throw an error?


def test_get_time3():
    assert get_time("10-23-19, 15:21") == time(15, 21)
