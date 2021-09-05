import PySimpleGUI as sg
from datetime import datetime as dt, date, timedelta
import db
from controller import update_results_table, update_summary, datestr_to_tuple, goto_date


def make_window():
    # style settings:
    sg.theme('Tan')
    med_btn = (10, 2)
    dummy_row = [None, None, None, None]
    default_date = (11, 1, 2015)


    # layouts
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
                     [sg.Check("Search Message Content"), sg.Check("Search Notes")],
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

    notes_area = sg.Col([[sg.Input("notes", size=(30, 50)), sg.B("commit")]])

    date_layout = [
        [sg.B(" < ", k="prev-day-btn"), sg.T('---, -- ---------- ----', font=("Helvetica 16 italic"), k="-DATEHEADER_OUT-"),
         sg.In(k="-DATE2-", visible=False, enable_events=True),  # hide this field
         sg.CalendarButton(" v ", format="%Y-%m-%d", target="-DATE2-", default_date_m_d_y=default_date, k='calbtn'),
         sg.T(" "), sg.B(" > ", k="next-day-btn")],
        [sg.T('')],
        [sg.T("Available Conversations", font=("Helvetica 12 bold"))],
        [sg.Listbox(values=["--", "--"], k="-CONVOLIST-"), sg.B("update")],
        [sg.B("Show msg notes", k="-TOGGLE_NOTES-", enable_events=True)],
        [chat_area]
    ]

    layout = [[sg.Text('ChatViewer Application (demo)--', size=(38, 1), justification='left', font=("Helvetica 16 bold"),
                k='-TEXT_HEADING-', enable_events=True)]]
    layout += [[sg.TabGroup([[sg.Tab('Main', main_layout),
                              sg.Tab('Date View', date_layout),
                              sg.Tab('Search', search_layout)
                              ]], k='-TABGROUP-', expand_x=True, expand_y=True)]]

    return sg.Window('ChatViewer Demo', layout, finalize=True)


def make_notes_window():
    layout = [[sg.T("From (name)", k='-nw_MSGNAME-'), sg.T("at 00:00: ", k="-nw_MSGTIME-")],
              [sg.T("Fetched msg content here", k="-nw_MSGCONTENT-"),
              [sg.T("")],
              [sg.Multiline("Notes here:", size=(30, 10), k="-nw_NOTEBOX-")],
               sg.B("Save", k="nw_commit-note-btn")]]

    return sg.Window("Message Notes", layout, margins=(10,10), finalize=True)


def main():
    # variables:
    conn = db.get_db()
    fname = None
    current_date = db.get_earliest_date(conn)
    current_msg_id = None
    main_window = make_window()
    notes_window = None

    # Event loop
    while True:
        event, values = main_window.read()  # values == keys
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # search tab
        elif event == "search-btn":
            search_term = values["-SEARCH-"].strip()
            # backend processes search
            if values['-SEARCH-'].strip() != "":
                update_results_table(search_term, main_window, conn)
        # TODO - add checkbox filters

        # main dashboard - import file pop up
        elif event == "import-btn":
            fname = sg.popup_get_file('Document to open', file_types=(("Text files", "*.txt"),))
            if fname:
                try:
                    print(fname)  # replace with loadfile()
                    sg.popup("Successful import! Import info")
                    update_summary(main_window)
                    fname = None
                except:
                    sg.popup("Import error - ")
        elif event == "refresh-btn":
            update_summary(main_window)
            main_window['calbtn'].default_date_m_d_y = datestr_to_tuple(db.get_earliest_date(conn))
        # TODO - add elif event == "delete-all-data-btn"

        # date-view eventhandlers
        elif event == '-DATE2-':
            if values['-DATE2-'] not in (None, ""):
                try:
                    # reformat date for header
                    current_date = values['-DATE2-']
                    goto_date(current_date, main_window)
                    # TODO - delete this
                    #date_heading = dt.strftime(dt.fromisoformat(current_date), "%A, %d %B %Y")
                    #window['-DATEHEADER_OUT-'].update(date_heading)
                    #update_chat_table(current_date, window)
                except ValueError:
                    print("some error happened")
                    pass
        elif event == "-CHAT_TABLE-":
            if main_window['-CHAT_TABLE-'].metadata is not None:
                current_msg_id = main_window['-CHAT_TABLE-'].metadata[values['-CHAT_TABLE-'][0]]
                print(f"current msg id is {current_msg_id}")
        elif event == "-TOGGLE_NOTES-":
            # show pop up window

            # event2, values2 = notes_window.read()
            while True:
                if event in (sg.WIN_CLOSED, 'Exit'):
                    thewindow.close()
                    if thewindow == notes_window:  # if closing win 2, mark as closed
                        notes_window = None
                    elif thewindow == main_window:  # if closing win 1, mark as closed
                        main_window = None
                elif current_msg_id is not None:
                    msg_item = db.read_msg(current_msg_id, conn)
                    print(msg_item)
                    #  update notes box + display
                    notes_window['-nw_MSGNAME-'].update(f"From {msg_item['speaker_name']}")
                    notes_window['-nw_MSGTIME-'].update(f"at {msg_item['date_time']}")
                    notes_window['-nw_MSGCONTENT-'].update(msg_item['msg_content'])
                    notes_window['-nw_NOTEBOX-'].update(msg_item['msg_notes'])
                elif event == "nw_commit-note-btn":
                    print("btn working")
                    break
            notes_window.close()

        elif event == "next-day-btn":
            # fetch date of next day
            next_day = date.fromisoformat(current_date) + timedelta(days=1)     # next_day is a datetime.date obj
            current_date = next_day.isoformat()
            goto_date(current_date, main_window)
        elif event == "prev-day-btn":
            # fetch date of prev day
            prev_day = date.fromisoformat(current_date) - timedelta(days=1)  # prev_day is a datetime.date obj
            current_date = prev_day.isoformat()
            goto_date(current_date, main_window)
    main_window.close()


if __name__ == "__main__":
    main()


