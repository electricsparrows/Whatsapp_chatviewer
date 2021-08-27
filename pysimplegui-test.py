import PySimpleGUI as sg

sg.theme('Tan')
'''
layout = [[sg.Text('Primary Button: ')],
          [sg.T(" ")],
          [sg.Button('Hello World', size=(20, 4))],
          [sg.Checkbox('check this', default= True, key="-IN-")]]
'''

# reusable UI
# btn_set1 = [sg.Ok(), sg.Cancel()]

# define window contents
# show this in a pop up or something
import_file = [
              [sg.T(" ")],
              [sg.T("Choose a File:   "), sg.In(key="-PATH-"),
               sg.FileBrowse(file_types= (("Text files", "*.txt"),))],
              [sg.T(" ")], [sg.Submit("Submit", k="path-btn"), sg.Cancel()]
              ]


# settings:
btn_med = (14, 2)


layout = [  [sg.T("ChatViewer Application -- ", font=("Helvetica 14 bold"))],
            [sg.T("")],
            [sg.Input(key="-SEARCH-"), sg.Submit("Search >", k="search-btn")],
            [sg.Text("_"*100)],
            [sg.Text("At a Glance...", font=("Helvetica 16 italic"))],
            [sg.B("Import File", k="import-btn")],
            [sg.T(""), sg.T("", k="-OUTPUT1-")],
            [sg.B("First message: ....", k="-FIRST_M-"), sg.B("Last message:...", k="-LAST_M-")],
            [sg.CalendarButton("  Select Date  ", target="-DATE-", format="%Y-%m-%d"),
             sg.Input(key="-DATE-"), sg.Submit(" Go ", k="date-btn")],
            [sg.T("")],
            []  # calendar heatmap
            ]

search_frame = [[sg.Input(key="-SEARCH-"), sg.Submit("Search >", k="search-btn")],
               []]  #some table

#add import file button somewhere
# - use vertical separator

date_view = sg.Column([
             [sg.T('')],
             [sg.T('')],
             [sg.T("Available Conversations", font=("Helvetica 14 bold"))],
             [],
             []
            ])


# create window
window = sg.Window('ChatViewer', layout, size= (600, 400))


# process data
def dummy_readfile(path):
    # validate path
    with open(path, mode='r', encoding='utf-8') as f:
        foo = f.readlines(5)
        print(foo)


if __name__ == "__main__":
    # variables:
    fname = None
    # Event loop
    while True:
        event, values = window.read()       # values == keys
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # event handlers ------
        elif event == "date-btn":
            date = values["-DATE-"]
            # get messages at date

        elif event == "search-btn":
            pass
        elif event == "import-btn":
            fname = sg.popup_get_file('Document to open', file_types=(("Text files", "*.txt"),))
            if fname:
                print(fname)    # replace with loadfile()
                sg.popup("Successful import! Import info")
                # update "at a glance" variables
                # fetch 
                window['-OUTPUT1-'].update(fname)
    window.close()

