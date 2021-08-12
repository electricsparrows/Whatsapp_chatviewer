import sqlite3

from typing import List

import message


def get_db():
    try:
        conn = sqlite3.connect("chatviewer.db")
        return conn
    except sqlite3.Error:
        return "problem with connecting to database"


def insert_parsed(conn, parsed_tuples: List[tuple]):
    cur = conn.cursor()

    # create tables
    cur.execute('''CREATE TABLE IF NOT EXISTS Messages
                    (msg_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    file_id INTEGER,
                    date_time datetime,
                    speaker_name TEXT, 
                    msg_content TEXT,
                    msg_notes TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Tag 
                    (msg_id INTEGER, 
                     tag_name TEXT unique,
                     PRIMARY KEY(msg_id, tag_name))''')

    # insert list of messages
    cur.executemany('''INSERT INTO Messages(file_id, date_time, speaker_name, msg_content) 
                        VALUES (?, ?, ?, ?)''', parsed_tuples)
    # print(cur.fetchall())
    conn.commit()


def describe(conn):
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM Messages')
    total_msgs = cur.fetchone()
    cur.execute('SELECT COUNT(distinct(speaker_name)) FROM Messages')
    num_speakers = cur.fetchone()


def read_msg(conn, msg_id: str):
    cur = conn.cursor()
    query = (msg_id,)
    cur.execute('SELECT * FROM Messages where msg_id = ?', query)
    return cur.fetchone()


def get_msgs_at_date(conn, formatted_date: str):
    cur = conn.cursor()
    query = (formatted_date,)
    cur.execute("SELECT * FROM Messages where STRFTIME('%Y-%m-%d', date_time) = ?", query)
    return cur.fetchall()


def get_msgs_from_date_range(conn, date1: str, date2: str):
    """
        Returns a list of message objects dated between date1 and date2 (exclusive)
        :param date1: start date range
        :param date2: end date range (exclusive)
        :param msgs: list of message objects
        :return: filtered list of messages
    """
    pass


def get_first_message(conn):
    cur = conn.cursor
    cur.execute("""SELECT * FROM Messages
                WHERE date_time = (SELECT MIN(date_time) from Messages)""")
    return cur.fetchone()


def get_last_message(conn):
    # might return two messages sometimes if timestamps clash -- not essential fix
    cur = conn.cursor
    cur.execute("""SELECT * FROM Messages
                    WHERE date_time = (SELECT MAX(date_time) from Messages)""")
    return cur.fetchone()


def get_yoy_activity(conn) -> dict:
    """
    returns message count per absolute date
    :param conn:
    :return:
    """
    cur = conn.cursor()
    cur.execute("""SELECT strftime('%Y-%m-%d', date_time) as valYear, COUNT(msg_id)
                    FROM Messages
                    GROUP BY valYear
                    ORDER BY valYear""")
    return cur.fetchall()


def add_note(conn, msg_id: int, note: str):
    cur = conn.cursor()
    cur.execute("UPDATE Messages SET msg_notes = ? WHERE msg_id = ?", (note, msg_id))
    conn.commit()


def get_note(conn, msg_id: int):
    cur = conn.cursor()
    cur.execute("SELECT msg_notes from Messages WHERE msg_id = ?", (msg_id,))
    conn.commit()


def add_tag(conn, msg_id: int, tag_name: str):
    '''
    :param conn: connection to database
    :param msg_id: id of target message
    :param tag_name:  tag name should be a string with no whitespaces.
    :return:
    '''
    cur = conn.cursor()
    tag = tag_name.strip()
    cur.execute("INSERT INTO TAG VALUES (?, ?)", (msg_id, tag))
    conn.commit()


def get_tags(conn, msg_id: str):
    cur = conn.cursor()
    query = (msg_id,)
    cur.execute("SELECT tag_name FROM TAG WHERE msg_id = ?", query)
    return cur.fetchall()


def remove_tag(conn, msg_id: str, tag_name: str):
    cur = conn.cursor()
    tag_name = tag_name.strip()
    cur.execute("DELETE FROM Tag WHERE msg_id = ? AND tag_name = ?", (msg_id, tag_name))
    conn.commit()


def retrieve_by_keyword(conn, search_term: str):
    cur = conn.cursor()
    search_term = search_term.strip()
    pass


def msg_wrapper(t: tuple) -> message.Message:
    return message.Message(t[0], t[1], t[2], t[3], t[4], t[5])


