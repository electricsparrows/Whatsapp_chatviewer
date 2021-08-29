import PySimpleGUI as sg
from datetime import datetime as dt
import db


def make_window():
    # style settings:
    sg.theme('Tan')
    med_btn = (10, 2)
    dummy_row = [None, None, None, None]
    default_date = (11, 1, 2015)

    main_layout = [
        [sg.Text("Main Dashboard", font=("Helvetica 16 italic"))],
        [sg.B("Import File", k="import-btn"), sg.B("Refresh", k="refresh-btn")],
        [sg.Frame("At a Glance...", [
            [sg.T("Total message count: ", k="-TOTAL_MSG-")],
            [sg.T("Number of participants: ", k="-NUM_PPL-")],
            [sg.T("First message: ....", k="-FIRST_M-")],
            [sg.T("Last message:...", k="-LAST_M-")]
            ], font= ("Helvetica 12 italic"))],
        [sg.CalendarButton("  Select Date  ", target="-DATE1-", format="%Y-%m-%d"),
        sg.Input(key="-DATE1-"), sg.Submit(" Go ", k="date-btn")],
        [sg.T("")],
        []  # calendar heatmap
    ]

    search_layout = [
                     [sg.T("Search Logs: ", font=("Helvetica 16 bold"))],
                     [sg.T()],
                     [sg.Input(default_text="Search Chat Logs", key="-SEARCH-"),
                      sg.Submit("  Search Messages >  ", k="search-btn")],
                     [sg.Table(values=[dummy_row], headings=["Time", "Name", "Content", "Notes"],
                              visible_column_map=[True, True, True, True],
                              expand_x=True,
                              background_color='black',
                              display_row_numbers=True,
                              justification='right',
                              alternating_row_color='black',
                              key='-RESULTS_TABLE-', row_height=30)]
                    ]   # some results table

    chat_area = sg.Col([[sg.Table(values=[dummy_row], headings=["Time", "Name", "Content", "Notes"],
                                  visible_column_map=[True, True, True, False],
                                  # col_widths = [0, 2, 2, 100, 40],
                                  auto_size_columns=True,
                                  expand_x=True,
                                  display_row_numbers=False,
                                  justification='left',
                                  background_color='#e5d7db',
                                  alternating_row_color='#e5d7db',
                                  enable_events=True,
                                  metadata=None,
                                  key='-CHAT_TABLE-', row_height=30)]], expand_x=True)

    date_layout = [
        [sg.T('---, -- ---------- ----', font=("Helvetica 16 italic"), k="-DATEHEADER_OUT-"),
         sg.In(k="-DATE2-", visible=False, enable_events=True),  # hide this field
         sg.CalendarButton(" v ", format="%Y-%m-%d", target="-DATE2-", default_date_m_d_y=default_date, k='calbtn')],
        [sg.T('')],
        [sg.T("Available Conversations", font=("Helvetica 12 bold"))],
        [sg.Listbox(values=["--", "--"], k="-CONVOLIST-")],
        [sg.B("Show msg notes", k="-TOGGLE_NOTES-", enable_events=True)],
        [chat_area],
        [sg.B(" < ", k="prev-day-btn", size=med_btn), sg.T(" "*120), sg.B(" > ", k="next-day-btn", size= med_btn)]
    ]

    layout = [[sg.Text('ChatViewer Application (demo)--', size=(38, 1), justification='left', font=("Helvetica 16 bold"),
                k='-TEXT_HEADING-', enable_events=True)]]
    layout += [[sg.TabGroup([[sg.Tab('Main', main_layout),
                              sg.Tab('Date View', date_layout),
                              sg.Tab('Search', search_layout)
                              ]], k='-TABGROUP-', expand_x=True, expand_y=True)]]

    return sg.Window('ChatViewer Demo', layout, finalize=True)


# eventhandlers
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
    """Transforms records from db_output (dictionaries) into lists, as required by PySimpleGUI's table element
    :param db_output: message records from db call in type dictionary
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
    """"Converts a datestr in isoformat to three-tuple(m,d,y)"""
    return (datestr[5:7], datestr[8:10], datestr[0:3])


def render_message_rows(data):
    """ Render list of dictionary type message records, into a column object
    :param data: message records from db call in type dictionary
    """
    lt = []
    for m in data:
        time = dt.strptime(m["date_time"], "%Y-%m-%d %H:%M:%S")   # add error handling
        time = time.strftime("%H:%M")
        mid = m['msg_id']
        # render each row, append to the column object.
        row = [sg.T(time), sg.T(m['speaker_name']), sg.T(m['msg_content']),
               sg.T(m['msg_id'], k= f"-MID_{mid}-", visible=True)]
        lt.append(row)
    # try window.extend_layout()
    return lt


def goto_date(date, window):
    """
    Updates window GUI components to display data associated with given date
    :param date: date string
    :return:
    """
    event, values = window.read()
    if date is not None:
        try:
            # reformat date for header display
            date_heading = dt.strftime(dt.strptime(values['-DATE2-'], "%Y-%m-%d"), "%A, %d %B %Y")
            window['-DATEHEADER_OUT-'].update(date_heading)
            # fetch convo list
            # fetch messages
            update_chat_table(values['-DATE2-'], window)
        except ValueError:
            print("some error happened")
            pass


def main():
    # variables:
    conn = db.get_db()
    fname = None
    current_date = db.get_earliest_date(conn)
    window = make_window()

    # Event loop
    while True:
        event, values = window.read()  # values == keys
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # search tab
        elif event == "search-btn":
            search_term = values["-SEARCH-"].strip()
            # backend processes search
            if values['-SEARCH-'].strip() != "":
                update_results_table(search_term, window, conn)

        # main dashboard - import file pop up
        elif event == "import-btn":
            fname = sg.popup_get_file('Document to open', file_types=(("Text files", "*.txt"),))
            if fname:
                try:
                    print(fname)  # replace with loadfile()
                    sg.popup("Successful import! Import info")
                    update_summary(window)
                    fname = None
                except:
                    sg.popup("Import error - ")
        elif event == "refresh-btn":
            update_summary(window)
            window['calbtn'].default_date_m_d_y = datestr_to_tuple(db.get_earliest_date(conn))

        # date-view eventhandlers
        elif event == '-DATE2-':
            if values['-DATE2-'] not in (None, ""):
                try:
                    # reformat date for header
                    current_date = values['-DATE2-']
                    date_heading = dt.strftime(dt.strptime(current_date, "%Y-%m-%d"), "%A, %d %B %Y")
                    window['-DATEHEADER_OUT-'].update(date_heading)
                    # fetch convo list
                    # fetch messages
                    update_chat_table(current_date, window)
                except ValueError:
                    print("some error happened")
                    pass
        elif event == "-CHAT_TABLE-":
            if window['-CHAT_TABLE-'].metadata is not None:
                msg_id = window['-CHAT_TABLE-'].metadata[values['-CHAT_TABLE-'][0]]
                print(msg_id)
        elif event == "-TOGGLE_NOTES-":
            print("working")
            # popup window to display notes
            # window.read()
        elif event == "next-day-btn":
            print("next day")
            # fetch date of next day
            # go to next day
        elif event == "prev-day-btn":
            print("prev day")
            # fetch date of prev day
            # go to next day
    window.close()

if __name__ == "__main__":
    main()


