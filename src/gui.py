from logging.handlers import QueueHandler
import queue
import threading
from handler import QueueHandler
import tkinter as tk

from parser_enum import Status
from tkinter import ttk, scrolledtext, Tk
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
from convert import ExcelConverter
from translator import GptService


class Gui:
    def __init__(self, main: Tk):
        self.main = main
        self.main.title("AAS Submodel json to excel converter")
        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(0, weight=1)

        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)

        vertical_pane = ttk.PanedWindow(self.main, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)

        # load button
        button_frame = ttk.Frame(horizontal_pane)
        button_frame.columnconfigure(0, weight=1)
        self.button = LoadButton(button_frame, self.queue_handler)
        horizontal_pane.add(button_frame, weight=1)

        # log box
        log_frame = ttk.Frame(horizontal_pane)
        log_frame.columnconfigure(0, weight=1)
        self.log_box = LogBox(log_frame, self.log_queue)
        horizontal_pane.add(log_frame, weight=1)

        self.main.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self, *args):
        self.main.destroy()
        self.button.stop_thread()


class LoadButton:
    def __init__(self, frame: ttk.Frame, queue_handler: QueueHandler):
        self.frame = frame
        self.button = ttk.Button(
            self.frame,
            text="JSON 파일 불러오기",
            command=lambda: self.on_convert(queue_handler),
        )
        self.button.grid(column=1, row=2, sticky=W, padx=10, pady=10, ipadx=5, ipady=5)
        self.stop_event = threading.Event()

    def on_convert(self, queue_handler):
        gpt = GptService()
        converter = ExcelConverter(translator=gpt)

        thread = threading.Thread(target=self.run, args=(converter, queue_handler))
        thread.start()

    def run(self, converter: ExcelConverter, queue_handler: QueueHandler):
        converter.jsons = converter.load_json_file()
        converter.convert_json_to_excel(queue_handler)

    def stop_thread(self):
        self.stop_event.set()


class LogBox:
    def __init__(self, frame: ttk.Frame, log_queue: queue):
        self.log_queue = log_queue
        self.frame = frame
        self.scrolled_text = scrolledtext.ScrolledText(
            frame, wrap=tk.WORD, state=tk.DISABLED
        )
        self.scrolled_text.grid(row=0, column=0)
        self.frame.after(100, self.polling)

    def polling(self):
        while True:
            try:
                message = ""
                log = self.log_queue.get(block=False)
                status = next(iter(log.values()))
                path = next(iter(log.keys()))
                if isinstance(status, Status):
                    message = f"{status.value} {path}\n"
            except queue.Empty:
                break
            else:
                self.display(message)
        self.frame.after(100, self.polling)

    def display(self, message):
        self.scrolled_text.configure(state=tk.NORMAL)
        self.scrolled_text.insert(tk.END, message)
        self.scrolled_text.config(state=tk.DISABLED)
        self.scrolled_text.yview(tk.END)
