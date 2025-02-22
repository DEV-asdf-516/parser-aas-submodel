from gui import Gui
import tkinter as tk


def main():
    root = tk.Tk()
    app = Gui(root)
    app.main.mainloop()


if __name__ == "__main__":
    main()
