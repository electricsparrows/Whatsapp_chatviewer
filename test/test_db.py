import sqlite3
from sqlite3 import Connection

import pytest

import db
from db import *


def get_conn():
    conn: Connection = sqlite3.connect("test.db")
    return conn


def test_insert_parsed():
    conn = get_conn()
    with conn:
        data_tuples = [('f1', '2010-08-13 13:30', 'Bill', 'Hi.'),
                      ('f1', '2010-08-13 13:30', 'Grace', 'Hey! Whats up?'),
                      ('f1', '2010-08-13 13:40', 'Bill', 'Nothing much.')]
        insert_parsed(conn, data_tuples)


def test_read_msg():
    conn = get_conn()
    with conn:
        result = read_msg(conn, 2)
        print(result)
    assert result == (2, 'f1', '2010-08-13 13:30', 'Grace', 'Hey! Whats up?', None)


def test_get_msg_by_date():
    assert True


def test_get_first_message():
    conn = get_conn()
    with conn:
        result = get_first_message(conn)
    assert result == (2, 'f1', '2010-08-13 13:30', 'Bill', 'Hi.', None)


def test_get_last_message():
    conn = get_conn()
    with conn:
        result = get_last_message(conn)
    assert result == (2, 'f1', '2010-08-13 13:40', 'Bill', 'Nothing much.', None)


def test_get_note():
    conn = get_conn()
    with conn:
        result = get_note(conn, 2)
        print(result)
    assert result is None


def test_add_note():
    conn = get_conn()
    with conn:
        test_note = "Sample annotation"
        add_note(conn, 1, test_note)
        result = get_note(conn, 1)
    assert result == [('Sample annotation',)]


def test_add_tag():
    conn = get_conn()
    with conn:
        test_tag = 'test   '
        add_tag(conn, 1, test_tag)
        result = get_tags(conn, 1)
    assert result == ('test',)


def test_get_tags():
    conn = get_conn()
    with conn:
        result = get_tags(conn, 1)
    assert result == ('test',)


def test_remove_tag():
    conn = get_conn()
    with conn:
        remove_tag(conn, 1, 'Sample annotation')
        result = get_tags(conn, 1)
        print(result)
