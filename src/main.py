from gui import Gui
from dotenv import load_dotenv
import tkinter as tk


def main():
    root = tk.Tk()
    app = Gui(root)
    app.main.mainloop()


if __name__ == "__main__":
    load_dotenv()
    main()
