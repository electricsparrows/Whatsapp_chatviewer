import PySimpleGUI as sg
from datetime import datetime as dt, date, timedelta
import db
from controller import update_results_table, update_summary, datestr_to_tuple, goto_date, open_msg_record
import filehandler as fh


def make_window():
    # style settings:
    sg.theme('Tan')
    med_btn = (10, 2)
    dummy_row = [None, None, None, None]
    default_date = (11, 1, 2015)


    # layouts
    main_layout = [
        [sg.Text("Main Dashboard", font=("Helvetica 16 italic"))],
        [sg.B("Import File", k="import-btn"), sg.B("Refresh", k="refresh-btn"), sg.B("Delete all", k="data-wipe-btn")],
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

    date_layout = [
        [sg.B(" < ", k="prev-day-btn"), sg.T('---, -- ---------- ----', font=("Helvetica 16 italic"), k="-DATEHEADER_OUT-"),
         sg.In(k="-DATE2-", visible=False, enable_events=True),  # field hidden
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
                     keep_on_top=True, metadata="notes")


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
            if fname:
                try:
                    fh.loadfile(fname)
                    sg.popup("Successful import! Import info")
                    update_summary(main_window)
                    fname = None
                except:
                    sg.popup("Import error - ")
        elif event == "refresh-btn":
            update_summary(main_window)
            main_window['calbtn'].default_date_m_d_y = datestr_to_tuple(db.get_earliest_date(conn))
        elif event == "data-wipe-btn":
            confirm = sg.popup_ok_cancel("Are you sure you want to delete all data?")
            if confirm == "OK":
                db.delete_all_msg(conn)

        # date-view eventhandlers
        elif event == '-DATE2-':
            if values['-DATE2-'] not in (None, ""):
                try:
                    current_date = values['-DATE2-']
                    goto_date(current_date, main_window)
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
                    print(window.metadata)  # this returns 'main'
                    open_msg_record(notes_window, msg)  # change focus to notes_window

        elif event == "-TOGGLE_NOTES-" and not notes_window:
            # show pop up second window
            notes_window = make_notes_window()

        elif event == "nw_commit-note-btn" and current_msg_id is not None:
            # collect input from multiline element
            new_note = values["-nw_NOTE_BOX-"].rstrip()
            # commit notes to db
            print(new_note)
            db.add_note(current_msg_id, new_note, conn)
            # update text to say "saved!"
            notes_window["-nw_COMMIT_MESSAGE-"].update(visible=True)

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


