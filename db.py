import sqlite3

from typing import List


def get_db():
    conn = sqlite3.connect("chatviewer.db")
    return conn


def insert_parsed(conn, parsed_tuples: List[tuple]):
    # conn = sqlite3.connect("chatviewer.db")
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
    cur.executemany('''INSERT INTO Messages(date_time, speaker_name, msg_content) 
                        VALUES (?, ?, ?)''', parsed_tuples)
    # print(cur.fetchall())
    conn.commit()


def read_msg(conn, msg_id: str):
    cur = conn.cursor
    query = (msg_id,)
    cur.execute('SELECT * FROM Messages where msg_id = ?', query)
    return cur.fetchone()


def get_msg_by_date(conn, date_str: str):
    cur = conn.cursor
    query = (date_str,)
    cur.execute('SELECT * FROM Messages where date_time = ?', query)
    return cur.fetchall()


def get_first_message():
    # SELECT MIN(date_time) FROM MESSAGES
    pass


def get_last_message():
    # SELECT MAX(date_time) FROM MESSAGES
    pass


def add_note(conn, msg_id: str, note: str):
    cur = conn.cursor()
    cur.execute("UPDATE Messages SET msg_notes = ? WHERE msg_id = ?", (note, msg_id))
    conn.commit()


# TODO test this
def add_tag(msg_id: int, tag_name: str):
    conn = sqlite3.connect("chatviewer.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO TAG VALUES (?, ?)", (msg_id, tag_name))
    conn.commit()


# TODO test this
def get_tag(conn, msg_id: str):
    conn = sqlite3.connect("chatviewer.db")
    cur = conn.cursor()
    query = (msg_id,)
    cur.execute("SELECT tag_name FROM TAG WHERE msg_id = ?", query)
    return cur.fetchall()


def remove_tag(msg_id: str, tag_name: str):
    conn = sqlite3.connect("chatviewer.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM Tag WHERE msg_id = ? AND tag_name = ?", (msg_id, tag_name))
    conn.commit()


# TODO refactor out the connection variable


