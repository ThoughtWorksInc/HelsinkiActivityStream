import logging
import sched
import time


class Scheduler:
    def __init__(self, interval, clock, stop_when, event):
        self._interval = interval
        self._clock = clock
        self._stopping_condition = stop_when
        self._s = sched.scheduler(clock.now, clock.delay)
        self._event = event

    def schedule_event(self):
        def event():
            if not self._stopping_condition():
                self._event()
                logging.info("Event scheduled at: " + self._clock.human_readable_time())
                self._s.enter(self._interval, 1, self.schedule_event())

        return event

    def start(self):
        self._s.enter(self._interval, 1, self.schedule_event())
        self._s.run()
        print("Stopping time: ", self._clock.now())


class Clock:
    def __init__(self):
        self.now = time.time
        self.delay = time.sleep
        self.human_readable_time = time.ctime


def stop_after(the_clock, seconds):
    stop_time = the_clock.now() + seconds

    def stop_when():
        return the_clock.now() > stop_time

    return stop_when
