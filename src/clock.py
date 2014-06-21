import time


class Clock(object):
    """Clock keeps track of the elapsed time and how much sleep is needed.

    frametime -- is the time that should pass between calls.
    """
    def __init__(self, frametime):
        super(Clock, self).__init__()
        self.frametime = frametime
        self.t0 = None

    def start(self):
        """Initialises the timer"""
        self.t0 = time.time()

    def sleep(self):
        t1 = time.time()
        td = t1 - self.t0
        if td < self.frametime:
            #print "sleeping %s" % (self.frametime - td)
            time.sleep(self.frametime - td)
        self.t0 = t1

    def left(self):
        t1 = time.time()
        td = t1 - self.t0
        return self.frametime - td