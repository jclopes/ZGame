import time


class Clock(object):
    """Clock keeps track of the elapsed time and how much sleep is needed.

    frametime -- is the time (in seconds) that should pass between calls.
    """
    def __init__(self, frametime):
        super(Clock, self).__init__()
        self.frametime = frametime
        self.t0 = None

    def start(self):
        """Initialises the timer"""
        self.t0 = time.time()

    def sleep(self):
        time.sleep(self.time_left())
        self.t0 = time.time()

    def time_left(self):
        res = 0.0
        t1 = time.time()
        td = t1 - self.t0
        if td < self.frametime:
            res = (self.frametime - td)
        return res

    def time_passed(self):
        return time.time() - self.t0

    def reset(self):
        self.start()
