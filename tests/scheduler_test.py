import unittest
import openahjo_activity_streams.scheduler as oas_s


class StubClock:
    def __init__(self, now=0):
        self._now = now

    def now(self):
        return self._now

    def delay(self, seconds):
        self._now += seconds


def later_than(clock, stopping_time):
    def stop_when():
        return clock.now() > stopping_time

    return stop_when


class SchedulerTest(unittest.TestCase):
    def test_schedules_and_runs_some_events_then_exits(self):
        clock = StubClock()
        s = oas_s.Scheduler(interval=1, clock=clock, stop_when=later_than(clock, 5))

        assert clock.now() == 0
        assert s.number_of_executed_events() == 0

        s.start()

        assert clock.now() >= 5
        assert s.number_of_executed_events() > 0


if __name__ == '__main__':
    unittest.main()
