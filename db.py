import random
import sqlite3

from typing import List

import message

# TODO -- flask tutorial actually has tips on how to write this


def get_db():
    try:
        conn = sqlite3.connect("chatviewer.db")
        return conn
    except sqlite3.Error:
        return None


def insert_parsed(conn, parsed_tuples: List[tuple]):
    """
    Creates Tables and inserts parsed message content into 'Message' Table
    :param conn:  database connection
    :param parsed_tuples:  output from parser, each tuple contains message elements
    :return:
    """
    cur = conn.cursor()

    # create tables
    cur.execute('''CREATE TABLE IF NOT EXISTS Messages
                    (msg_id     INTEGER PRIMARY KEY AUTOINCREMENT, 
                    conv_id     INTEGER,
                    import_ref  INTEGER,
                    date_time   datetime,
                    speaker_name    TEXT, 
                    msg_content     TEXT,
                    msg_notes   TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Tag 
                    (msg_id INTEGER, 
                     tag_name TEXT unique,
                     PRIMARY KEY(msg_id, tag_name))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Conversation
                    (conv_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     participants TEXT NOT NULL,
                     start_time datetime
                     end_time datetime)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS TagList
                    (tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     tag_name TEXT unique not null)''')

    # insert list of messages
    cur.executemany('''INSERT INTO Messages(import_ref, date_time, speaker_name, msg_content) 
                        VALUES (?, ?, ?, ?)''', parsed_tuples)
    # print(cur.fetchall())
    conn.commit()


def execute_query(conn, querystring):
    cur = conn.cursor()
    cur.execute(querystring).fetchall()


def generate_import_ref(conn):
    # fetch the last import ref
    cur = conn.cursor()
    last = cur.execute('SELECT max(import_ref) FROM MESSAGES').fetchone()
    if last is not None:
        return last[0] + 1
    # increment
    else:
        # return a random number
        return random.randint(10)


def summary(conn):
    """
    Returns a dict with summary statistics giving a general picture of the
    state of the attached database
    - total messages, no. of speakers, no. of conversation threads
    :param conn: database connection obj
    :return:
    """
    result = {}
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM Messages')
    result['total_msgs'] = cur.fetchone()[0]
    cur.execute('SELECT COUNT(distinct(speaker_name)) FROM Messages')
    result['num_speakers'] = cur.fetchone()[0]
    cur.execute('SELECT COUNT(distinct(convo_id)) FROM Messages')
    result['num_convos'] = cur.fetchone()[0]
    return result


def read_msg(conn, msg_id: str):
    """
    Retrieve message record by given msg_id
    :param conn: database connection
    :param msg_id: message id
    :return:
    """
    cur = conn.cursor()
    query = (msg_id,)
    cur.execute('SELECT * FROM Messages where msg_id = ?', query)
    return cur.fetchone()


def get_msgs_at_date(conn, formatted_date: str):
    cur = conn.cursor()
    query = (formatted_date,)
    cur.execute("SELECT * FROM Messages where STRFTIME('%Y-%m-%d', date_time) = ?", query)
    return cur.fetchall()


def get_msgs_from_date_range(conn, start_date: str, end_date: str):
    """
        Returns a list of message objects dated between date1 and date2 (exclusive)
        :param start_date: start date range
        :param end_date: end date range (exclusive)
        :return: filtered list of messages tuples
    """
    # TODO
    res = []
    # check dates are valid: start_date < end_date
    # get list of dates between range
    conn = get_db()
    # query the database in one go
    # return results.
    current_date = start_date
    while current_date < end_date:
        try:
            # this will incur multiple scans
            res += get_msgs_at_date(conn, str(current_date))
            current_date.increment()
        except:
            print(f"date {current_date} not found")
    return res


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


def get_tags(conn, msg_id: int):
    cur = conn.cursor()
    query = (msg_id,)
    cur.execute("SELECT tag_name FROM TAG WHERE msg_id = ?", query)
    return cur.fetchall()


def remove_tag(conn, msg_id: int, tag_name: str):
    cur = conn.cursor()
    tag_name = tag_name.strip()
    cur.execute("DELETE FROM Tag WHERE msg_id = ? AND tag_name = ?", (msg_id, tag_name))
    conn.commit()


def retrieve_by_keyword(conn, qstr: str):
    cur = conn.cursor()
    qstr = f'%{qstr.strip()}%'
    cur.execute("SELECT * From Messages WHERE msg_content LIKE ? ESCAPE '\'", (qstr,))
    return cur.fetchall


def msg_wrapper(t: tuple) -> message.Message:
    return message.Message(t[0], t[1], t[2], t[3], t[4], t[5])


