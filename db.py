import sqlite3


# connect database
conn = sqlite3.connect("datastore.db")

# create tables (if they don't exist yet)
with conn:
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Message
                    (msg_id INT, Date DATE, Time TIME, sender TEXT, msg_content TEXT)''')
    cur.execute('CREATE TABLE Tag (msg_id INT, tag_name TEXT)')
    cur.execute('CREATE TABLE Notes (msg_id INT, note TEXT)')


def add_message():
    pass


def read_message():
    pass


def add_tag():
    pass


def get_tag():
    pass


def remove_tag():
    pass




