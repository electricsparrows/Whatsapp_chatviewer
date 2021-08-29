import random
import sqlite3
from typing import List
import message as msg

# from sqlite documentation
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    try:
        conn = sqlite3.connect("chatviewer.db")
        conn.row_factory = dict_factory
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


def summary(conn=get_db()):
    """
    Returns a dict with summary statistics giving a general picture of the
    state of the attached database
    - total messages, no. of speakers, no. of conversation threads
    :param conn: database connection obj
    :return: dictionary where k: summary statistic name, v: value of statistic
    """
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as total_msgs FROM Messages')
    total_m = cur.fetchone()
    cur.execute('SELECT COUNT(distinct(speaker_name)) as num_speakers FROM Messages')
    num_speakers = cur.fetchone()
    # cur.execute('SELECT COUNT(distinct(conv_id)) as conversation_count FROM Messages')
    # num_convos = cur.fetchone()
    return {**total_m, **num_speakers}


def read_msg(msg_id: int, conn=get_db()):
    """
    Retrieves message record by given msg_id
    :param conn: database connection; connects to chatViewer.db by default
    :param msg_id: message id
    :return:
    """
    cur = conn.cursor().execute('SELECT * FROM Messages where msg_id = ?', (msg_id,))
    return cur.fetchone()


def get_msgs_at_date(formatted_date: str, conn=get_db()) -> List:
    """
    Retrieves message records associated with given date
    :param conn: database connection; connects to chatViewer.db by default
    :param formatted_date: date string given in ISO-8601 format (YYYY-MM-DD)
    :return: list of message records
    """
    cur = conn.cursor().execute("SELECT * FROM Messages where STRFTIME('%Y-%m-%d', date_time) = ?", (formatted_date,))
    return cur.fetchall()


def get_first_message(conn=get_db()):
    """
    Retrieves oldest message in the database
    :param conn: database connection; connects to chatViewer.db by default
    :return: 'message' data access object
    """
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Messages
                WHERE date_time = (SELECT MIN(date_time) from Messages)""")
    return cur.fetchone()


def get_last_message(conn=get_db()):
    """
    Retrieves newest message in the database
    :param conn: database connection; connects to chatViewer.db by default
    :return: 'message' data access object
    """
    # issue: might return two messages sometimes if timestamps clash -- not essential fix
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Messages
                    WHERE date_time = (SELECT MAX(date_time) from Messages)""")
    return cur.fetchone()


def get_message_count_by_date(conn=get_db()) -> dict:
    """
    returns message count per absolute date in each available year
    :param conn:
    :return: list of tuples -- (date, msg_count)
    """
    cur = conn.cursor().execute("""SELECT strftime('%Y-%m-%d', date_time) as valDate, COUNT(msg_id) as msg_count
                                    FROM Messages
                                    GROUP BY valDate
                                    ORDER BY valDate""")
    return cur.fetchall()


def get_message_count_by_year(conn=get_db()) -> dict:
    """
        returns message count per year
        :param conn: database connection; connects to chatViewer.db by default
        :return: dictionary with key-value pairs representing (year, msg_count)
    """
    cur = conn.cursor().execute("""SELECT strftime('%Y', date_time) as valYear, COUNT(msg_id) as msg_count
                        FROM Messages
                        GROUP BY valYear
                        ORDER BY valYear""")
    return cur.fetchall()


def add_note(msg_id: int, note: str, conn=get_db()):
    cur = conn.cursor()
    cur.execute("UPDATE Messages SET msg_notes = ? WHERE msg_id = ?", (note, msg_id))
    conn.commit()


def get_note(msg_id: int, conn=get_db()):
    cur = conn.cursor()
    cur.execute("SELECT msg_notes from Messages WHERE msg_id = ?", (msg_id,))
    conn.commit()


def remove_note(msg_id: int, conn=get_db()):
    cur = conn.cursor()
    cur.execute("UPDATE Messages SET msg_notes = NULL WHERE msg_id = ?", (msg_id,))
    conn.commit()


def add_tag(msg_id: int, tag_name: str, conn=get_db()):
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


def get_tags(msg_id: int, conn=get_db()):
    cur = conn.cursor()
    cur.execute("SELECT tag_name FROM TAG WHERE msg_id = ?", (msg_id,))
    return cur.fetchall()


def remove_tag(msg_id: int, tag_name: str, conn=get_db()):
    cur = conn.cursor()
    tag_name = tag_name.strip()
    cur.execute("DELETE FROM Tag WHERE msg_id = ? AND tag_name = ?", (msg_id, tag_name))
    conn.commit()


def keyword_search(querystr: str, conn=get_db()):
    cur = conn.cursor()
    qstr = f'%{querystr.strip()}%'
    cur.execute("SELECT * From Messages WHERE msg_content LIKE ? ESCAPE ? ", (qstr, "\\"))
    return cur.fetchall()


def get_earliest_date(conn=get_db()) -> str:
    cur = conn.cursor().execute("""SELECT strftime('%Y-%m-%d', 
                                   (SELECT Min(date_time) from Messages)) AS min_date FROM Messages""")
    return cur.fetchone()['min_date']


# could turn this into a row factory like flask.
def msg_wrapper(t: tuple):
    return msg.Message(t[0], t[1], t[2], t[3], t[4], t[5], t[6])


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


if __name__ == "__main__":
    print(get_msgs_at_date("2016-01-06"))