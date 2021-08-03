import sqlite3

from typing import List


def test_database_connection():
    conn = sqlite3.connect("chatviewer.db")
    with conn:
        cur = conn.cursor()

        # create tables
        cur.execute('''CREATE TABLE IF NOT EXISTS Messages
                        (msg_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         file_id INTEGER, 
                         datetime datetime, 
                         speaker TEXT, 
                         msg_content TEXT,
                         msg_notes TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Tag 
                        (msg_id INTEGER PRIMARY KEY, tag_name TEXT)''')

        cur.execute("INSERT INTO Tag VALUES(13, 'saved')")
        cur.execute("SELECT * FROM Tag")
        print(cur.fetchall())



def import_parsed(parsed_tuples: List[tuple]):
    conn = sqlite3.connect("chatviewer.db")
    cur = conn.cursor()

    # create tables
    cur.execute('''CREATE TABLE IF NOT EXISTS Messages
                    (msg_id INTEGER PRIMARY KEY AUTOINCREMENT, datetime datetime, speaker_name TEXT, msg_content TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Tag (msg_id INTEGER, tag_name TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Notes (msg_id INTEGER, note TEXT)''')

    # insert list of messages
    cur.executemany('''INSERT INTO Messages(datetime, speaker_label, msg_content) 
                        VALUES (?, ?, ?, ?)''', parsed_tuples)
    # print(cur.fetchall())

    conn.commit()


def read_message():
    cur.execute("""SELECT FROM Messages""")
    pass


def add_tag(msg_id: int, tag_name: str):
    conn = sqlite3.connect("chatviewer.db")
    with conn:
        cur = conn.cursor()

    # INSERT INTO Tag VALUES(
    pass


def get_tag():
    pass


def remove_tag():
    pass




