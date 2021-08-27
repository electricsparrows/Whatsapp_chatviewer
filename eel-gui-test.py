import eel 
from pathlib import Path
import sys
import db
from typing import List

web_dir = Path("C:\\Users\\Cindy\\PycharmProjects\\ChatViewer-testfiles\\web-test")

# set web files folder
eel.init(web_dir)

# Presentation Logic

# to send data from python --> javascript
@eel.expose
def display_data():
    data = "some data"
    return data


# to retrieve data from javascript --> python
@eel.expose
def get_filepath(fpath):
    with open(fpath, mode='r', encoding='utf-8') as f:
        f.readline(10)

# javascript send request to python
# triggers the function to retrieve the filepath

@eel.expose
def get_msgs_at_date(dt) -> List:
    return db.get_msgs_at_date(dt)


@eel.expose
def handle_exit(ar1,ar2):
   sys.exit(0)

# start app
if __name__ == "__main__":
    app_opt = {
        'mode': "chrome",
        'close_callback' : handle_exit
    }
    eel.start('templates/date-view.html', size= (600, 400), jinja_templates='templates')


# CODE DUMP
# {% include 'includes/_navbar.html' %}
# <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">