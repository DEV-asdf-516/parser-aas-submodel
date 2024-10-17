import queue


class QueueHandler:  # ui / 로직 동시작업
    def __init__(self, log_queue: queue):
        self.log_gueue = log_queue

    def add(self, log):
        self.log_gueue.put(log)
