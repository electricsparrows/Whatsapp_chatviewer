import random
import sqlite3

from typing import List

import message as msg


def get_db():
    try:
        conn = sqlite3.connect("chatviewer.db")
        return conn
    except sqlite3.Error:
        return None


def insert_parsed(parsed_tuples: List[tuple], conn=get_db()):
    """
    Creates Tables and inserts parsed message content into 'Message' Table
    :param conn:  database connection
    :param parsed_tuples:  output from parser, each tuple contains message elements
    :return:
    """
    cur = conn.cursor()

    # create tables
    cur.execute('''CREATE TABLE IF NOT EXISTS Messages
                    (msg_id         INTEGER PRIMARY KEY AUTOINCREMENT, 
                    conv_id         INTEGER,
                    import_ref      INTEGER,
                    date_time       datetime,
                    speaker_name    TEXT, 
                    msg_content     TEXT,
                    msg_notes       TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Tag 
                    (msg_id         INTEGER, 
                     tag_name       TEXT unique,
                     PRIMARY KEY(msg_id, tag_name))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Conversation
                    (conv_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                     participants   TEXT NOT NULL,
                     start_time     datetime
                     end_time       datetime)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS TagList
                    (tag_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                     tag_name       TEXT unique not null)''')

    # insert list of messages
    cur.executemany('''INSERT INTO Messages(import_ref, date_time, speaker_name, msg_content) 
                        VALUES (?, ?, ?, ?)''', parsed_tuples)
    conn.commit()


def generate_import_ref(conn=get_db()):
    # fetch the last import ref
    try:
        cur = conn.cursor()
        last = cur.execute('SELECT max(import_ref) FROM MESSAGES').fetchone()
        return int(last[0]) + 1
    except sqlite3.OperationalError:
        # return a random number
        return random.randint(0, 10)


def summary(conn= get_db()):
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
    cur.execute('SELECT COUNT(distinct(conv_id)) FROM Messages')
    result['num_convos'] = cur.fetchone()[0]
    return result


def read_msg(msg_id: int, conn = get_db()):
    """
    Retrieves message record by given msg_id
    :param conn: database connection; connects to chatViewer.db by default
    :param msg_id: message id
    :return:
    """
    cur = conn.cursor()
    query = (msg_id,)
    cur.execute('SELECT * FROM Messages where msg_id = ?', query)
    return cur.fetchone()


def get_msgs_at_date(formatted_date: str, conn= get_db()):
    """
    Retrieves message records associated with given date
    :param conn: database connection; connects to chatViewer.db by default
    :param formatted_date: date string given in ISO-8601 format (YYYY-MM-DD)
    :return: list of message records
    """
    cur = conn.cursor()
    query = (formatted_date,)
    cur.execute("SELECT * FROM Messages where STRFTIME('%Y-%m-%d', date_time) = ?", query)
    return [msg_wrapper(tup) for tup in cur.fetchall()]


def get_msgs_from_date_range(start_date: str, end_date: str, conn= get_db()):
    """
        Returns a list of message objects dated between date1 and date2 (exclusive)
        :param start_date: start date range
        :param end_date: end date range (exclusive)
        :return: filtered list of messages tuples
    """
    # De-scoped function
    res = []
    # check dates are valid: start_date < end_date
    # get list of dates between range
    # query the database in one go
    # return results.


def get_first_message(conn):
    """
    Retrieves oldest message in the database
    :param conn: database connection; connects to chatViewer.db by default
    :return: 'message' data access object
    """
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Messages
                WHERE date_time = (SELECT MIN(date_time) from Messages)""")
    return msg_wrapper(cur.fetchone())


def get_last_message(conn):
    """
    Retrieves newest message in the database
    :param conn: database connection; connects to chatViewer.db by default
    :return: 'message' data access object
    """
    # might return two messages sometimes if timestamps clash -- not essential fix
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Messages
                    WHERE date_time = (SELECT MAX(date_time) from Messages)""")
    return msg_wrapper(cur.fetchone())


def get_yoy_activity(conn) -> dict:
    """
    returns message count per absolute date in each available year
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


def remove_note(msg_id: int, conn=get_db()):
    cur = conn.cursor()
    cur.execute("UPDATE Messages SET msg_notes = NULL WHERE msg_id = ?", (msg_id,))
    conn.commit()

def add_tag(msg_id: int, tag_name: str, conn= get_db()):
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


def get_tags(msg_id: int, conn= get_db()):
    cur = conn.cursor()
    cur.execute("SELECT tag_name FROM TAG WHERE msg_id = ?", (msg_id,))
    return cur.fetchall()


def remove_tag(msg_id: int, tag_name: str, conn= get_db()):
    cur = conn.cursor()
    tag_name = tag_name.strip()
    cur.execute("DELETE FROM Tag WHERE msg_id = ? AND tag_name = ?", (msg_id, tag_name))
    conn.commit()


def keyword_search(querystr: str, conn= get_db()):
    cur = conn.cursor()
    qstr = querystr.strip()
    cur.execute("SELECT * From Messages WHERE msg_content LIKE ? ESCAPE '\'", (qstr,))
    return cur.fetchall


# could turn this into a row factory like flask.
def msg_wrapper(t: tuple) -> msg.Message:
    return msg.Message(t[0], t[1], t[2], t[3], t[4], t[5])


# This script i nicked from flask documentation
def query_db(query, args=(), one=False):
    cur = get_db().cursor().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if rv:
        if one:
            return msg_wrapper(rv[0])
        else:
            return [msg_wrapper(r) for r in rv]
    else:
        return None
    # return (rv[0] if rv else None) if one else rv

