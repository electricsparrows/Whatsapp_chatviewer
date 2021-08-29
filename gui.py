import PySimpleGUI as sg
from datetime import datetime as dt
import db

'''
layout = [[sg.Text('Primary Button: ')],
          [sg.T(" ")],
          [sg.Button('Hello World', size=(20, 4))],
          [sg.Checkbox('check this', default= True, key="-IN-")]]
'''


# define window contents


def make_window():
    # style settings:
    sg.theme('Tan')
    btn_med = (14, 2)

    """
    import_file = [
        [sg.T(" ")],
        [sg.T("Choose a File:   "), sg.In(key="-PATH-"),
         sg.FileBrowse(file_types=(("Text files", "*.txt"),))],
        [sg.T(" ")], [sg.Submit("Submit", k="path-btn"), sg.Cancel()]
    ]
    """

    main_layout = [
        #[sg.Input(key="-SEARCH2-"), sg.Submit("Search >", k="search-btn2")],
        #[sg.Text("_" * 100)],
        [sg.Text("Main Dashboard", font=("Helvetica 16 italic"))],
        [sg.B("Import File", k="import-btn"), sg.B("refresh", k="refresh-btn")],
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
                     [sg.Input(default_text="Search Chat Logs", key="-SEARCH-"), sg.Submit("  Search Messages >  ", k="search-btn")],
                     [sg.Column(layout=[],
                                k="-SEARCH_OUTPUT-", scrollable=True, vertical_scroll_only=True)]
                     ]   # some results table

    date_layout = [
        [sg.T('---, -- ---------- ----', font=("Helvetica 16 italic"), k="-DATEHEADER_OUT-"),
         sg.In(k="-DATE2-", visible=False),  # hide this field
         sg.CalendarButton(".", format=("%Y-%m-%d"), target="-DATE2-"), sg.Submit(" > ", k="date-header-btn")],
        [sg.T('')],
        [sg.T("Available Conversations", font=("Helvetica 12 bold"))],
        [sg.Listbox(values=["--", "--"], k="-CONVOLIST-")],
        [sg.Checkbox("Show msg notes", enable_events=True, k="-TOGGLE_NOTES-")],
        [sg.Table(values=[dummy_row], headings= ["msg_id", "Time", "Name", "Content", "Notes"],
                  visible_column_map= [False, True, True, True, False],
                  expand_x=True,
                  background_color='black',
                  display_row_numbers=False,
                  justification='right',
                  alternating_row_color='black',
                  key='-CHAT_TABLE-', row_height=25)],
        [sg.B(" < ", k="prev-day-btn"), sg.T(" "*100), sg.B(" > ", k="next-day-btn")]
    ]

    layout = [[sg.Text('ChatViewer Application (demo)--', size=(38, 1), justification='left', font=("Helvetica 16 bold"),
                k='-TEXT_HEADING-', enable_events=True)]]
    layout += [[sg.TabGroup([[sg.Tab('Main', main_layout),
                              sg.Tab('Date View', date_layout),
                              sg.Tab('Search', search_layout)
                              ]], k='-TABGROUP-', expand_x=True, expand_y=True)]]

    return sg.Window('ChatViewer Demo', layout, size= (600, 600), finalize=True)


# process data / eventhandlers
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
    data = db.get_msgs_at_date(date, conn)
    transformed_data = reformat_records(data)
    window['-CHAT_TABLE-'].update(values=transformed_data)


def reformat_records(db_output):
    """Transforms records from db_output (dictionaries) into lists, as required by PySimpleGUI's table element"""
    lt = []
    for dict in db_output:
        time = dt.strptime(dict["date_time"], "%Y-%m-%d %H:%M:%S")  # error handling
        time = time.strftime("%H:%M")
        row = [dict['msg_id'], time, dict['speaker_name'], dict['msg_content'], dict['msg_notes']]
        lt.append(row)
    return lt


def render_message_rows(data):
    """ Render list of dictionary type message records, into a column object"""
    lt = []
    for m in data:
        time = dt.strptime(m["date_time"], "%Y-%m-%d %H:%M:%S")   # error handling
        time = time.strftime("%H:%M")
        mid = m['msg_id']
        # render each row, append to the column object.
        row = [sg.T(time), sg.T(m['speaker_name']), sg.T(m['msg_content']),
               sg.T(m['msg_id'], k= f"-MID_{mid}-", visible=True)]
        lt.append(row)
    return lt


def goto_date(date):
    if date not in (None, window):
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
    pass


if __name__ == "__main__":
    # variables:
    fname = None
    dummy_row = [None, None, None, None, None]
    window = make_window()
    # Event loop
    while True:
        event, values = window.read()       # values == keys
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # search tab
        elif event == "search-btn":
            search_term = values["-SEARCH-"]
            print(search_term)
            # backend processes search
            msg_data = db.keyword_search(search_term)
            lt = render_message_rows(msg_data)
            window["-SEARCH_OUTPUT-"].update(lt)
            window.read()

        # main dashboard - import file pop up
        elif event == "import-btn":
            fname = sg.popup_get_file('Document to open', file_types=(("Text files", "*.txt"),))
            if fname:
                try:
                    print(fname)    # replace with loadfile()
                    sg.popup("Successful import! Import info")
                    update_summary(window)
                    fname = None
                except:
                    sg.popup("Import error - ")
        elif event == "refresh-btn":
            update_summary(window)

        # date-view eventhandlers
        elif event == "date-header-btn":
            if values['-DATE2-'] not in (None, ""):
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
        elif event == "-TOGGLE-NOTES-":
            pass
        elif event == "next-day-btn":
            pass
        elif event == "prev-day-btn":
            pass
    window.close()


