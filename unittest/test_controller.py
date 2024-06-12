import pytest
from controller import *


def get_test_conn():
    return


def test_stringify_datetup1():
    tup = (1, 9, 2014)
    datestr = stringify_datetup(tup)
    assert datestr == "2014-01-09"


def test_stringify_datetup2():
    tup = (10, 3, 2020)
    datestr = stringify_datetup(tup)
    assert datestr == "2020-10-03"


def test_stringify_datetup3():
    tup = (10, 13, 2020)
    datestr = stringify_datetup(tup)
    assert datestr == "2020-10-13"
