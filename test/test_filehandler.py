import pytest
from datetime import datetime, date, time
from filehandler import *

#TODO - unit testing for parser function
def parser():
    assert False


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
    # Shoud this throw an error?


def test_get_time3():
    assert get_time("10-23-19, 15:21") == time(15, 21)
