from threading import Condition, RLock, Thread


class WatchMonitor():
    def __init__(self, client):
        self.queue = []
        self.client = client
        self.mutex = RLock()
        self.notempty = Condition(self.mutex)
        self.kue = None

    def enqueue(self, item):
        with self.mutex:
            self.queue.append(item)
            self.notempty.notify()

    def dequeue(self):
        while True:
            with self.mutex:
                while len(self.queue) == 0:
                    self.notempty.wait()

                val = self.queue[0]
                print("Sending: " + val)
                self.client.sendall(val.encode())
                del self.queue[0]

    def run(self):
        self.kue = Thread(target=self.dequeue)
        self.kue.start()

    def close(self):
        if self.kue:
            self.kue.join()
