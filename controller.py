import db
from db import get_db, get_first_message, get_last_message, get_msgs_at_date, get_message_count_by_date, get_message_count_by_year
from datetime import datetime as dt
import PySimpleGUI as sg

# eventHandlers
def dummy_readfile(path):
    """ test function to validate path"""
    with open(path, mode='r', encoding='utf-8') as f:
        foo = f.readlines(5)
        print(foo)


def update_summary(window: sg.Window, conn= db.get_db()):
    """updates the "At a glance" variables"""
    data = db.summary(conn)
    # fetch data from database
    tmc = data['total_msgs']
    nop = data['num_speakers']
    first_m, last_m = db.get_first_message(conn), db.get_last_message(conn)
    name1, dt1 = first_m['speaker_name'], first_m['date_time']
    name2, dt2 = last_m['speaker_name'], last_m['date_time']
    print(tmc, nop, name1, dt1, name2, dt2)

    window['-TOTAL_MSG-'].update(f'Total message count: {tmc}')
    window['-NUM_PPL-'].update(f'Number of participants: {nop}')
    # update first and last messages as well
    window['-FIRST_M-'].update(f'First message: \nFrom {name1} at {dt1}')
    window['-LAST_M-'].update(f'Last message: \nFrom {name2} at {dt2}')
    # also update the activity charts...


def update_chat_table(date: str, window: sg.Window, conn= db.get_db()):
    """Populates the CHAT-TABLE element with records at given date from database"""
    data = db.get_msgs_at_date(date, conn)
    transformed_data, ids = reformat_records(data)
    window['-CHAT_TABLE-'].update(values=transformed_data)
    window['-CHAT_TABLE-'].metadata = ids


def reformat_records(db_output, search=False):
    """
    Transforms records from db_output (dictionaries) into lists, as required by PySimpleGUI's table element
    :param db_output: (type List[dict]), message records from db call
    :param search: (type bool), true if function used for search-results view, false if used for date-view;
                    search flag is set to false by default
    :return lt (type List[list]) list of message records info in form [time, name, ocntent, notes];
            ids (List[int]) list of corresponding msg_ids
    """
    lt = []
    ids = []
    fmt = "%H:%M"
    if search:
        fmt = "%Y-%m-%d, %H:%M"

    for dict in db_output:
        time = dt.strptime(dict["date_time"], "%Y-%m-%d %H:%M:%S")  # error handling
        time = time.strftime(fmt)
        row = [time, dict['speaker_name'], dict['msg_content'], dict['msg_notes']]
        lt.append(row)
        ids.append(dict['msg_id'])
    return lt, ids


def update_results_table(search_str, window, conn):
    """Populates the RESULTS-TABLE element with records at given date from database"""
    data = db.keyword_search(search_str, conn)
    data, ids = reformat_records(data, search=True)
    window["-RESULTS_TABLE-"].update(values=data)
    window["-RESULTS_TABLE-"].metadata = ids


def datestr_to_tuple(datestr):
    """"
    Converts a datestring in isoformat to three-tuple(%m,%d,%Y)
    """
    return (datestr[5:7], datestr[8:10], datestr[0:3])


def stringify_datetup(datetup):
    """Converts (m-d-Y) date tuple to string in isoformat ("%Y-%m-%d")"""
    Y = '{:04d}'.format(datetup[2])
    m = '{:02d}'.format(datetup[0])
    d = '{:02d}'.format(datetup[1])
    return f'{Y}-{m}-{d}'


def goto_date(date, window):
    """
    Updates window GUI components to display data associated with given date
    :param date: date string
    :param window: active window
    :return:
    """
    if date is not None:
        try:
            # reformat date for header display
            date_heading = dt.strftime(dt.fromisoformat(date), "%A, %d %B %Y")
            window['-DATEHEADER_OUT-'].update(date_heading)
            # fetch convo list
            # fetch messages
            update_chat_table(date, window)
        except ValueError:
            print("some error happened")
            pass


def open_msg_record(window: sg.Window, msg: dict):
    """
    Renders the record view for populating a msg record
    :param window: reference to the notes_window
    :param msg: message record retrieved from database
    :return:
    """
    window["-nw_MSG_NAME-"].update(f"From {msg['speaker_name']}")
    window["-nw_MSG_TIME-"].update(f"at  {msg['date_time']}")
    window["-nw_MSG_CONTENT-"].update(msg['msg_content'])
    window["-nw_NOTE_BOX-"].update("")
    window["-nw_NOTE_BOX-"].update(msg['msg_notes'])
    window["-nw_COMMIT_MESSAGE-"].update(visible=False)


# functions below are for the fall back interface; also for testing"""


def view_stats():
    conn = get_db()
    ov = db.summary(conn)
    # retrieve first message in DB
    first = get_first_message(conn)
    # retrieve last message in DB
    last = get_last_message(conn)
    return ov, first, last


def view_calendar():
    print("activity calendar view")
    conn = get_db()
    # info to be rendered
    count_year = get_message_count_by_year(conn)
    count_day = get_message_count_by_date(conn)
    return count_year, count_day
    # return dict {year : List[(date, #. of msgs for that date)}


def view_msgs_at_date():
    date_str = str(input("Enter a date (YYYY-MM-DD): >>> "))
    # input validation -- done in gui.
    # query DB -> List[msg_tups]
    conn = get_db()
    lt = get_msgs_at_date(conn, date_str)
    for rec in lt:
        print(rec['msg_id'], rec['datetime'], rec[''])


def select_msg(msg_id : str):
    msg_id = msg_id.strip()
    if msg_id.isdigit():
        msg_id = int(msg_id)
        # view commands for message
        """
        msg_cmd = {'s' : save,
                     't' : add tag,
                     'n' : annotate_msg}
        """


def view_from_beginning():
    conn = get_db()
    first_msg = get_first_message(conn)
    print("first message")


def search_by_keyword():
    query = input("Please enter a keyword: >>> ")
    # query string validation
    # query DB
    # render results:
    print("we found nothing :D")


def nav_menu():
    nav = {'a': prev_day, 'd': next_day,
           's': view_msgs_at_date, "m": main_menu}
    print("Navigation options:\n" +
          "- previous day   (a)\n" +
          "- next day       (d)\n" +
          "- select date    (s)\n" +
          "- back to main   (m)\n")

    nav_cmd = str(input("Pls enter a command: >>> "))
    nav_cmd = nav_cmd.strip()
    try:
        nav[nav_cmd]()
    except:
        print("no such command")


def main_menu():
    """fall back interface; also for testing"""
    nav_menu = {
        "s": view_stats,
        "c": NotImplemented,
        "d": view_msgs_at_date,
        "f": view_from_beginning,
        "r": search_by_keyword
    }

    running = True
    while running:
        print("Main menu:\n" +

              "- summary stats       (s)\n" +
              "- calendar view       (c)\n" +
              "- retrieve by date    (d)\n" +
              "- view from beginning (f)\n" +
              "- search messages     (r)")

        command = input("Enter a command: >>> ")
        command = str(command).strip()
        try:
            nav_menu[command]()

            while True:
                next_command = input("\n-- go back (b) or exit (exit)? >>> ")
                if next_command == 'b':
                    break
                elif next_command == "exit":
                    running = False
                    break
        except:
            if command == "exit":
                running = False
            else:
                print("no such command")

