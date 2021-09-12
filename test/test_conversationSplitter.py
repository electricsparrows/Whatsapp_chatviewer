import pytest
from conversationSplitter import conversation_splitter, convert_dtstr_to_datetime, has_greetings, calc_timedelta

def test_conversation_splitter():
    assert False


def test_convert_dtstr_to_datetime():
    assert False


def test_has_greetings01():
    arg = "Hi George! How have you been?"
    assert has_greetings(arg) is True


def test_has_greetings02():
    arg = "I left my umbrella in the stand this morning"
    assert has_greetings(arg) is False


def test_calc_timedelta():
    assert False
