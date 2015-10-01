import sched


class Scheduler:
    def __init__(self, interval, clock, stop_when):
        self._interval = interval
        self._clock = clock
        self._stopping_condition = stop_when
        self._s = sched.scheduler(clock.now, clock.delay)
        self._event_count = 0

    def number_of_executed_events(self):
        return self._event_count

    def schedule_event(self):
        def event():
            self._event_count += 1
            if not self._stopping_condition():
                self._s.enter(self._interval, 1, self.schedule_event())

        return event

    def start(self):
        self._s.enter(self._interval, 1, self.schedule_event())
        self._s.run()
        print("Number of events executed: ", self.number_of_executed_events())
        print("Stopping time: ", self._clock.now())
