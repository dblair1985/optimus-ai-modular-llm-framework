# File: C:/Omega/Optimus/main.py

from gui.tk_gui import launch_gui
from core.handler import process_input

if __name__ == "__main__":
    print("🚀 Starting Optimus...")
    launch_gui(callback=process_input)
