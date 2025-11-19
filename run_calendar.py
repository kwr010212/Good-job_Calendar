# run_calendar.py
from tkinter import Tk
from calendar_app import MintCalendarApp


def main():
    root = Tk()
    MintCalendarApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
