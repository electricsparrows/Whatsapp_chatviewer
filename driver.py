from datetime import datetime as dt
from pathlib import Path
import db
import filehandler as fh

# globals
test_files_dir = "C:\\Users\\Cindy\\PycharmProjects\\ChatViewer-testfiles"
p = Path(test_files_dir)

in_file = p / "test01.txt"
out_file = Path.cwd() / "out" / "output.xlsx"



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    file = fh.loadfile(in_file)
    # print("---------------------------------")
