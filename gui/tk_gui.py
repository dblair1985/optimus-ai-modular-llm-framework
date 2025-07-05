# File: C:/Omega/Optimus/gui/tk_gui.py

import tkinter as tk
from tkinter import ttk
from gui.tabs import tab_chat

class OptimusGUI:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback

        self.root.title("Optimus AI")
        self.root.geometry("1200x800")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.chat_tab = tab_chat.build(self)

    def send_input(self, user_input):
        result = self.callback(user_input)
        print(result)


def launch_gui(callback):
    root = tk.Tk()
    app = OptimusGUI(root, callback)
    root.mainloop()
