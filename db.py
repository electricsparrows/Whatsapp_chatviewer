import random
import sqlite3
from typing import List


# from sqlite documentation
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    try:
        conn = sqlite3.connect("chatviewer.db", timeout=10)
        conn.row_factory = dict_factory
        return conn
    except sqlite3.Error:
        print("connection error -- check database")
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
    cur.execute('''CREATE TABLE IF NOT EXISTS Messages(
                    msg_id          INTEGER PRIMARY KEY AUTOINCREMENT, 
                    conv_id         INTEGER,
                    import_ref      INTEGER,
                    date_time       datetime,
                    speaker_name    TEXT, 
                    msg_content     TEXT,
                    msg_notes       TEXT,
                    UNIQUE(date_time, speaker_name, msg_content)
                    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Tag 
                    (msg_id         INTEGER, 
                     tag_name       TEXT,
                     PRIMARY KEY(msg_id, tag_name))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Conversation
                    (conv_id        INTEGER PRIMARY KEY,
                     participants   TEXT NOT NULL,
                     start_time     datetime
                     end_time       datetime)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS TagList
                    (tag_id         INTEGER PRIMARY KEY,
                     tag_name       TEXT unique not null)''')

    # insert list of messages
    cur.executemany('''INSERT INTO Messages(import_ref, date_time, speaker_name, msg_content) 
                        VALUES (?, ?, ?, ?)''', parsed_tuples)
    conn.commit()


def generate_import_ref(conn=get_db()):
    """
    Returns a unique import reference.
    :param conn:
    :return:
    """
    try:
        cur = conn.cursor()
        if not messages_is_empty():
            # attempts to fetch the last import ref
            last = cur.execute('''SELECT max(import_ref) AS 'imp_ref' FROM MESSAGES''').fetchone()
        else:
            last = random.randint(0, 10)

        return last['imp_ref'] + 1

    except sqlite3.OperationalError:    # if tables don't exist yet
        # return a random number
        return random.randint(0, 10)


def messages_is_empty(conn=get_db()) -> bool:
    """ Indicates whether the database/ message table is currently empty"""
    cur = conn.cursor().execute("""SELECT * FROM Messages""").fetchall()
    return len(cur) == 0


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


def get_conversation_msgs(formatted_date: str, ptr, conn=get_db()):
    """
    :param formatted_date:
    :param ptr: ptr is a msg_id reference which points to conversation head message record.
    :param conn:
    :return:
    """
    head = read_msg(ptr, conn)
    data = get_msgs_at_date(formatted_date, conn)
    # filter by import reference
    data = filter(lambda m: m['import_ref'] == head['import_ref'], data)
    # filter by time


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


def get_message_count_by_dateyear(year: int, conn=get_db()) -> dict:
    """
    returns message count per absolute date in each available year
    :param conn:
    :return: dictionary with key-value pairs corresponding to <isoformat date_str: message count (int)>
    """
    cur = conn.cursor().execute("""SELECT strftime('%Y-%m-%d', date_time) as valDate, 
                                          COUNT(msg_id) as msg_count
                                    FROM Messages
                                    WHERE strftime('%Y', valDate) = ?
                                    GROUP BY valDate
                                    ORDER BY valDate""", (str(year),))
    # tidy the return data format into a single dictionary
    rv = cur.fetchall()
    res = {}
    for r in rv:
        res[r['valDate']] = r['msg_count']
    return res


def get_message_count_by_year(conn=get_db()) -> dict:
    """
        returns message count per year
        :param conn: database connection; connects to chatViewer.db by default
        :return: dictionary with key-value pairs representing <year_str: str, msg_count (int) >
    """
    cur = conn.cursor().execute("""SELECT strftime('%Y', date_time) as valYear, COUNT(msg_id) as msg_count
                                    FROM Messages
                                    GROUP BY valYear
                                    ORDER BY valYear""")
    rv = cur.fetchall()   # list of dictionaries
    res = {}
    for r in rv:
        res[r['valYear']] = r['msg_count']
    return res


def add_note(msg_id: int, note: str, conn=get_db()):
    cur = conn.cursor()
    cur.execute("UPDATE Messages SET msg_notes = ? WHERE msg_id = ?", (note, msg_id))
    conn.commit()


def get_note(msg_id: int, conn=get_db()) -> str:
    cur = conn.cursor()
    cur.execute("SELECT msg_notes from Messages WHERE msg_id = ?", (msg_id,))
    return cur.fetchone()['msg_notes']


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
    try:
        cur.execute("INSERT INTO TAG VALUES (?, ?)", (msg_id, tag))
        conn.commit()
    except sqlite3.IntegrityError:
        pass    #do nothing


def get_tags(msg_id: int, conn=get_db()) -> List[str]:
    """
    Returns a list of tags tagged to message record with given msg_id
    :param msg_id: reference to message record
    :param conn: database connection; default is get_db()
    :return: list of tag names
    """
    cur = conn.cursor().execute("SELECT tag_name FROM TAG WHERE msg_id = ?", (msg_id,))
    rv = cur.fetchall()
    return [item['tag_name'] for item in rv]


# TODO - fix locked database
def remove_tag(msg_id: int, tag_name: str, conn=get_db()):
    tag_name = tag_name.strip()
    # need to check the tag to remove is present
    cur = conn.cursor()
    if tag_name in get_tags(27, conn):
        cur.execute("DELETE FROM Tag WHERE msg_id = ? AND tag_name = ?", (msg_id, tag_name))
        conn.commit()


def keyword_search(keyword: str, conn=get_db()):
    param = (keyword, filter)
    cur = conn.cursor()
    qstr = f'%{keyword.strip()}%'
    cur.execute("SELECT * From Messages WHERE msg_content LIKE ? ESCAPE ? ", (qstr, "\\"))
    return cur.fetchall()


def get_earliest_date(conn=get_db()) -> str:
    cur = conn.cursor().execute("""SELECT strftime('%Y-%m-%d', 
                                   (SELECT Min(date_time) from Messages)) AS min_date FROM Messages""")
    return cur.fetchone()['min_date']


def delete_all_msg(conn=get_db()):
    cur = conn.cursor().execute("""DELETE FROM Messages""")
    conn.commit()


# This script i nicked from the flask documentation
def query_db(query, args=(), one=False):
    cur = get_db().cursor().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == "__main__":
    #print(get_message_count_by_dateyear(2018))
    print(messageStore_is_empty())