import PySimpleGUI as sg
from datetime import datetime as dt, date, timedelta
import db
from controller import update_results_table, update_summary, datestr_to_tuple, goto_date, open_msg_record, \
    stringify_datetup, update_chat_table
import filehandler as fh
import conversationSplitter


def make_window():
    # style settings:
    sg.theme('Tan')
    font_heading = ("Comic 16 italic")
    font_body = "Comic"
    med_btn = (10, 2)
    dummy_row = [None, None, None, None]
    def_date = (1, 11, 2015)

    # layouts
    main_layout = [
        [sg.Text("Main Dashboard", font=font_heading)],
        [sg.B("Import File", k="import-btn"), sg.B("Refresh", k="refresh-btn"), sg.B("Delete all", k="data-wipe-btn")],
        [sg.Frame("At a Glance...", [
            [sg.T("Total message count: ", k="-TOTAL_MSG-")],
            [sg.T("Number of participants: ", k="-NUM_PPL-")],
            [sg.T("First message: ....", k="-FIRST_M-")],
            [sg.T("Last message:...", k="-LAST_M-")]
            ], font= ("Helvetica 12 italic"))],
        []  # TODO - embed activity heatmap
    ]

    search_layout = [
                     [sg.T("Search Logs: ", font=font_heading)],
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

    date_header = sg.Col([[sg.T('---, -- ---------- ----', font=font_heading, k="-DATEHEADER_OUT-"),
                           sg.In(k="-DATE-", visible=False, enable_events=True),      # field hidden
                           sg.B(" v ", k="select-date-btn")]])
    date_layout = [
        [sg.B(" < ", k="prev-day-btn"), sg.T(""*10), date_header, sg.T(""*10), sg.B(" > ", k="next-day-btn")],
        [sg.T("Available Conversations", font=("Helvetica 12 bold"))],
        [sg.Listbox(values=[], size= (30, 3), k="-CONVOLIST-", enable_events=True),
         sg.T(" ", expand_x=True),
         sg.B("Show msg notes", k="-TOGGLE_NOTES-")],
        [chat_area]
    ]

    layout = [[sg.Text('ChatViewer Application (demo)--', size=(38, 1), justification='left', font=("Helvetica 16 bold"),
                k='-TEXT_HEADING-')]]
    tab_padding = (50, 100)
    layout += [[sg.TabGroup([[sg.Tab('Main', main_layout),
                              sg.Tab('Date View', date_layout),
                              sg.Tab('Search', search_layout)
                              ]], k='-TABGROUP-', expand_x=True, expand_y=True)]]

    return sg.Window('ChatViewer Demo', layout, finalize=True, metadata="main")


def make_notes_window():
    layout = [[sg.T("From ----", k="-nw_MSG_NAME-"), sg.T("at --:-- ", k="-nw_MSG_TIME-")],
              [sg.T(" "), sg.T("Fetched msg content here", k="-nw_MSG_CONTENT-")],
              [sg.Multiline(size=(50, 5), k="-nw_NOTE_BOX-",
                            no_scrollbar=True,
                            expand_x=True, expand_y=True,
                            do_not_clear=False)],
              [sg.B("Save", k="nw_commit-note-btn"), sg.T("saved!", k="-nw_COMMIT_MESSAGE-", visible=False)]]

    return sg.Window("Message Notes", layout, margins=(10, 10), finalize=True,
                     keep_on_top=True, metadata="notes", resizable=True)
                    # TODO - add tagging function


def main():
    # variables:
    conn = db.get_db()      # connection to relevant database
    fname = None            # file path to retrieve file to be imported from
    current_date = None     # current date is the 'date' date-view will update according to. (format: %Y-%m-%d)
    current_msg_id = None   # msg_id of the current selected message

    main_window = make_window()        # main window
    notes_window = None                # window of the add/view notes popup

    if not db.messages_is_empty():
        current_date = db.get_earliest_date(conn)

    # Event loop
    while True:
        window, event, values = sg.read_all_windows()  # values == keys
        if window == sg.WIN_CLOSED:                    # if all windows were closed
            break
        if event in (sg.WIN_CLOSED, 'Exit'):
            window.close()
            if window == notes_window:  # if closing notes window, mark as closed
                notes_window = None
            elif window == main_window:  # if closing main window, exit program
                break

        # search tab
        elif event == "search-btn":
            search_term = values["-SEARCH-"].strip()
            if search_term != "":
                update_results_table(search_term, main_window, conn)
        # TODO - add checkbox filters

        # main dashboard - import file pop up
        elif event == "import-btn":
            fname = sg.popup_get_file('Document to open', file_types=(("Text files", "*.txt"),))
            # TODO - input path can currently be edited - need to block that/ error handling
            if fname:
                #try:
                    fh.loadfile(fname)
                    sg.popup("Successful import! Import info")
                    #update_summary(main_window)
                    fname = None
                #except:
                    #sg.popup("Import error - ")

        elif event == "refresh-btn":
            # add handling for no records
            update_summary(main_window)
            current_date = db.get_earliest_date(conn)

        elif event == "data-wipe-btn":
            confirm = sg.popup_ok_cancel("Are you sure you want to delete all data?")
            if confirm == "OK":
                db.delete_all_msg(conn)

        # date-view eventhandlers
        elif event == '-DATE-':
            if values['-DATE-'] not in (None, ""):
                try:
                    current_date = values['-DATE-']
                    goto_date(current_date, main_window, conn)
                except ValueError:
                    print("some error happened")
                    pass
        elif event == "-CHAT_TABLE-":
            if main_window['-CHAT_TABLE-'].metadata is not None:
                # fetch msg_id of current row
                current_msg_id = main_window['-CHAT_TABLE-'].metadata[values['-CHAT_TABLE-'][0]]
                print(f"current msg id is {current_msg_id}")    # for debugging use
                msg = db.read_msg(current_msg_id, conn)
                if notes_window is not None:
                    #  update notes box + display
                    print(window.metadata)              # this returns 'main'
                    open_msg_record(notes_window, msg)  # change focus to notes_window

        elif event == "-TOGGLE_NOTES-" and not notes_window:
            # show pop up second window
            notes_window = make_notes_window()

        elif event == "nw_commit-note-btn" and current_msg_id is not None:
            # collect input from multiline element
            new_note = values["-nw_NOTE_BOX-"].rstrip()
            # commit notes to db
            db.add_note(current_msg_id, new_note, conn)
            # update text to say "saved!"
            notes_window["-nw_COMMIT_MESSAGE-"].update(visible=True)

        elif event == "next-day-btn":
            # fetch date of next day
            next_day = date.fromisoformat(current_date) + timedelta(days=1)     # next_day is a datetime.date obj
            current_date = next_day.isoformat()
            goto_date(current_date, main_window, conn)
        elif event == "prev-day-btn":
            # fetch date of prev day
            prev_day = date.fromisoformat(current_date) - timedelta(days=1)  # prev_day is a datetime.date obj
            current_date = prev_day.isoformat()
            goto_date(current_date, main_window, conn)

        elif event == "select-date-btn":
            m_d_Y = sg.popup_get_date(start_mon=9, start_year=2015, no_titlebar=True)
            if m_d_Y is not None:
                current_date = stringify_datetup(m_d_Y)
                goto_date(current_date, main_window, conn)

        elif event == "-CONVOLIST-":
            selected_cvhead = values["-CONVOLIST-"][0][1]   # value returns [(datetime stamp, msg_id)]
            # get truncated messages list at given date
            msgs = db.get_msgs_at_date(current_date, conn)
            update_chat_table(msgs, window, conn, selected_cvhead)

    main_window.close()


if __name__ == "__main__":
    main()



