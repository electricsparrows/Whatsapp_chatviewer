import db
from db import get_db, msg_wrapper, get_first_message, get_last_message, get_msgs_at_date, get_yoy_activity


def view_stats():
    print("Viewing stats")
    conn = get_db()
    db.summary()
    # retrieve first message in DB
    first_msg = msg_wrapper(get_first_message(conn))
    # retrieve last message in DB
    last_msg = msg_wrapper(get_last_message(conn))
    # print summmary stats
    print (first_msg, last_msg)


def view_calendar():
    print("activity calendar view")
    conn = get_db()
    lt = get_yoy_activity(conn)
    # return dict {year : List[(date, #. of msgs for that date)}


def view_msgs_at_date():
    date_str = str(input("Enter a date (YYYY-MM-DD): >>> "))
    # input validation (pass from 'view module'
    # format string:
    # query DB -> List[msg_tups]
    conn = get_db()
    lt = get_msgs_at_date(conn, date_str)
    for mtup in lt:
        msg = msg_wrapper(mtup)
        # pass to GUI to render
    # print nav commands


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
    first_msg = msg_wrapper(get_first_message(conn))
    print("first message")
    # open relevant conversation
    # render (in GUI)
    # load commands()


def search_by_keyword():
    query = input("Please enter a keyword: >>> ")
    # query string validation
    # query DB
    # render results:
    print("we found nothing :D")


def prev_day():
    NotImplemented
    pass


def next_day():
    NotImplemented
    pass


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
    nav_menu = {
        "s": view_stats,
        "c": view_calendar,
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
