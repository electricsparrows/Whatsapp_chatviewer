import tkinter as tk
from tkinter import filedialog, ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('MyApp name')
        self.geometry('600x400')
        self.resizable(False, False)


fileimport = ttk.Frame()


if __name__ == "__main__":
    app = App()