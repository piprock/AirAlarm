from datetime import datetime

from regions import TEST_ALARM_TIME, NEXT_TEST_ALARM_AFTER


class State:
    def __init__(self, city):
        self.region_name = city
        self.SirenaNowPlaying = False
        self.SirenaPlayed = False
        self.end = 0
        self.MusicPlaying = False
        self.alarmNotification = 0
        self.testing = False
        self._test_alarm_started_at = datetime.now()

    def reset_test_alarm(self):
        self._test_alarm_started_at = datetime.now()

    def is_test_alarm(self):
        now_relative_to_first_start = datetime.now() - self._test_alarm_started_at
        now_relative_to_every_start = now_relative_to_first_start % (TEST_ALARM_TIME + NEXT_TEST_ALARM_AFTER)
        return now_relative_to_every_start < TEST_ALARM_TIME
