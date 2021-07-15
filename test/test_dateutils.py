import pytest
from dateutils import *


def test_get_date():
    d = Date(datetime(2012, 1, 12))
    assert (str(d) == "2012-01-12")


def test_is_leap_year():
    d = Date(datetime(2000, 1, 1))
    test = [2000, 1900, 2016, 2012, 2008, 2012, 2017, 2020, 2003, 1995, 1800]
    expected = [True, False, True, True, True, True, False, True, False, False, False]
    for i in range(len(test)):
        assert d.is_leap_year(test[i]) == expected[i]


def test_get_next_date():
    testcases = [Date(datetime(2012, 1, 12)),
                 Date(datetime(2020, 7, 31)),
                 Date(datetime(2011, 12, 31)),
                 Date(datetime(2019, 2, 27)),
                 Date(datetime(2019, 2, 28)),
                 Date(datetime(2015, 4, 30))]
    outcomes = ["2012-01-13 00:00:00", "2020-08-01 00:00:00", "2012-01-01 00:00:00",
                "2019-02-28 00:00:00", "2019-03-01 00:00:00", "2015-05-01 00:00:00"]
    for i in range(len(testcases)):
        test = testcases[i]
        expected = outcomes[i]
        assert (str(test.get_next_date()) == expected)


def test_get_prev_date():
    testcases = [Date(datetime(2012, 1, 12)),
                 Date(datetime(2020, 8, 1)),
                 Date(datetime(2012, 1, 1)),
                 Date(datetime(2019, 2, 27)),
                 Date(datetime(2019, 3, 1)),
                 Date(datetime(2015, 5, 1))]
    outcomes = ["2012-01-11 00:00:00", "2020-07-31 00:00:00", "2011-12-31 00:00:00",
                "2019-02-26 00:00:00", "2019-02-28 00:00:00", "2015-04-30 00:00:00"]
    for i in range(len(testcases)):
        test = testcases[i]
        expected = outcomes[i]
        assert (str(test.get_prev_date()) == expected)


def test_leapYearCases_get_next_date():
    positive_cases = [Date(datetime(2020, 2, 28)), Date(datetime(2016, 2, 28)), Date(datetime(2014, 2, 28)),
                      Date(datetime(2008, 2, 28)), Date(datetime(2004, 2, 28)), Date(datetime(2000, 2, 28))]
    negative_cases = [Date(datetime(2017, 2, 28)), Date(datetime(1900, 2, 28)), Date(datetime(2013, 2, 28)),
                      Date(datetime(2002, 2, 28))]
    pos_outcome = ["2020-02-29 00:00:00", "2016-02-29 00:00:00", "2014-02-29 00:00:00",
                   "2008-02-29 00:00:00", "2004-02-29 00:00:00", "2000-02-29 00:00:00"]
    neg_outcome = ["2017-03-01 00:00:00", "1900-03-01 00:00:00", "2013-03-01 00:00:00", "2002-03-01 00:00:00"]
    all_cases = positive_cases + negative_cases
    all_outcomes = pos_outcome + neg_outcome
    for i in range(len(all_cases)):
        test = all_cases[i]
        expected = all_outcomes[i]
        assert (str(test.get_next_date()) == expected)


def test_leapYearCases_get_prev_date():
    positive_cases = [Date(datetime(2020, 3, 1)), Date(datetime(2016, 3, 1)), Date(datetime(2014, 3, 1)),
                      Date(datetime(2008, 3, 1)), Date(datetime(2004, 3, 1)), Date(datetime(2000, 3, 1))]
    negative_cases = [Date(datetime(2017, 3, 1)), Date(datetime(1900, 3, 1)), Date(datetime(2013, 3, 1)),
                      Date(datetime(2002, 3, 1))]
    pos_outcome = ["2020-02-29 00:00:00", "2016-02-29 00:00:00", "2014-02-29 00:00:00",
                   "2008-02-29 00:00:00", "2004-02-29 00:00:00", "2000-02-29 00:00:00"]
    neg_outcome = ["2017-02-28 00:00:00", "1900-02-28 00:00:00", "2013-02-28 00:00:00", "2002-02-28 00:00:00"]
    all_cases = positive_cases + negative_cases
    all_outcomes = pos_outcome + neg_outcome
    for i in range(len(all_cases)):
        test = all_cases[i]
        expected = all_outcomes[i]
        assert (str(test.get_prev_date()) == expected)


def test_increment01():
    d1 = Date(datetime(2015, 12, 31))
    d1.increment()
    assert(str(d1) == "2016-01-01")


def test_increment02():
    d1 = Date(datetime(2020, 6, 24))
    for i in range(10):
        d1.increment()
    assert(str(d1) == "2020-07-04")


def test_decrement01():
    d1 = Date(datetime(2020, 7, 1))
    d1.decrement()
    assert(str(d1) == "2020-06-30")


def test_decrement02():
    d1 = Date(datetime(2020, 1, 31))
    for i in range(50):
        d1.decrement()
    assert (str(d1) == "2019-12-12")