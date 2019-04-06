import time


class Timer(object):
    def __init__(self):
        self.start_time = 0
        self.is_running = False

    def start(self):
        self.start_time = time.time()
        self.is_running = True

    def reset(self):
        self.start_time = time.time()

    def get(self) -> float:
        if self.is_running:
            return time.time() - self.start_time
        else:
            return 0.0

    def has_passed(self, period) -> bool:
        if self.get() >= period:
            self.reset()
            return True
        else:
            return False

    def stop(self):
        self.is_running = False
