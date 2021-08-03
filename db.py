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


def insert_parsed(parsed_tuples: List[tuple]):
    conn = sqlite3.connect("chatviewer.db")
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


def read_message():
    cur.execute("""SELECT FROM Messages""")
    pass

# TODO test this
def add_tag(msg_id: int, tag_name: str):
    conn = sqlite3.connect("chatviewer.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO TAG VALUES (?, ?)", (msg_id, tag_name))
    conn.commit()


def save_message(msg_id: int):
    add_tag(msg_id, "saved")


# TODO test this
def get_tag(msg_id: str):
    conn = sqlite3.connect("chatviewer.db")
    cur = conn.cursor()
    query = (msg_id,)
    cur.execute("SELECT tag_name FROM TAG WHERE msg_id = ?", query)
    conn.commit()


def remove_tag(msg_id: str):
    conn = sqlite3.connect("chatviewer.db")
    pass


# TODO refactor out the connection variable


