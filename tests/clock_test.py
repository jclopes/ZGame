from unittest import TestCase
from zgame.clock import Clock
import time


class ClockTest(TestCase):
    """unittests for ClockTest"""
    def test_time_pass_time_left(self):
        """Checks that values return by time_left and time_passed are
        coherent.
        """
        frameTime = 0.3
        c = Clock(frameTime)
        c.start()
        time.sleep(0.1)
        timeLeft = c.time_left()
        timePassed = c.time_passed()
        self.assertTrue(
            (timePassed + timeLeft > 0.29) and
            (timePassed + timeLeft < 0.31)
        )
        self.assertTrue(timePassed > 0.09 and timePassed < 0.11)
        self.assertTrue(timeLeft > 0.19 and timeLeft < 0.21)
