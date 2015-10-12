import unittest
import time
import openahjo_activity_streams.scheduler as oas_s


class StubClock:
    def __init__(self, now=0):
        self._now = now

    def now(self):
        return self._now

    def delay(self, seconds):
        self._now += seconds

    def human_readable_time(self):
        return time.ctime()


def later_than(clock, stopping_time):
    def stop_when():
        return clock.now() > stopping_time

    return stop_when


class Event:
    def __init__(self):
        self._called = False

    def execute(self):
        self._called = True

    def was_called(self):
        return self._called


class SchedulerTest(unittest.TestCase):
    def setUp(self):
        self.clock = StubClock()
        self.event = Event()

    def test__schedules_and_runs_some_events_then_exits(self):
        s = oas_s.Scheduler(interval=1, clock=self.clock, stop_when=later_than(self.clock, 5), event=self.event.execute)

        self.assertEquals(self.clock.now(), 0)
        self.assertFalse(self.event.was_called())

        s.start()

        self.assertGreaterEqual(self.clock.now(), 5)
        self.assertTrue(self.event.was_called())

    def test__does_not_run_event_if_stopping_condition_is_met(self):

        s = oas_s.Scheduler(interval=1, clock=self.clock, stop_when=later_than(self.clock, 0), event=self.event.execute)

        self.assertFalse(self.event.was_called())
        s.start()
        self.assertFalse(self.event.was_called())


if __name__ == '__main__':
    unittest.main()
