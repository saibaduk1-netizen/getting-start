from queue import Queue

class CommandQueue:
    def __init__(self):
        self.queue = Queue()

    def put(self, cmd):
        self.queue.put(cmd)

    def get(self, timeout=None):
        return self.queue.get(timeout=timeout)
    