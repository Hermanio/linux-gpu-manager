import time

from modes.Action import Action
from modes.Governor import Governor


class PerformanceGovernor(Governor):
    """
    Runs the GPU at specified "boost" clock speed if requested.
    """

    def __init__(self):
        super().__init__()
        self.GOVERNOR_NAME = 'PERFORMANCE_GOVERNOR'

        self.LOW_TEMP_LIMIT = 70
        self.SAFE_TEMP_LIMIT = 80
        self.CRITICAL_TEMP_LIMIT = 90

        # Intel HD4000 has 50MHZ steppings, setting them will automatically
        self.SMALL_MHZ_STEPPING = 50
        self.BIG_MHZ_STEPPING = 200

        self.GOVERNOR_POLL_PERIOD_IN_SECONDS = 0.5

    def start(self):
        """
        Starts the governor main loop.
        :return:
        """

        print("Starting governor {:s}...".format(self.GOVERNOR_NAME))

        # main loop
        while True:
            # get action
            action = self.decide_action()

            # apply action
            self.apply_action(action)

            # print status
            # self.get_status()

            # sleep... I need some, too
            time.sleep(self.GOVERNOR_POLL_PERIOD_IN_SECONDS)

    def apply_action(self, action):
        """
        Apply settings.
        :param min:
        :param stock:
        :param max:
        :return:
        """
        if action == Action.THROTTLE_MODERATE:
            clock_change = -self.SMALL_MHZ_STEPPING
        elif action == Action.THROTTLE_CRITICAL:
            clock_change = -self.BIG_MHZ_STEPPING
        elif action == Action.BOOST_MODERATE:
            clock_change = self.SMALL_MHZ_STEPPING
        elif action == Action.BOOST_CRITICAL:
            clock_change = self.BIG_MHZ_STEPPING
        elif action == Action.NO_OP:
            clock_change = 0
        else:
            clock_change = 0

        self.CURRENT_CLOCK_LIMIT = self.CURRENT_CLOCK_LIMIT + clock_change

        if self.CURRENT_CLOCK_LIMIT < self.DEFAULT_MIN_CLOCK:
            self.CURRENT_CLOCK_LIMIT = self.DEFAULT_MIN_CLOCK

        if self.CURRENT_CLOCK_LIMIT > self.DEFAULT_MAX_CLOCK:
            self.CURRENT_CLOCK_LIMIT = self.DEFAULT_MAX_CLOCK

        # min, max, boost
        settings = {
            "min": self.DEFAULT_MIN_CLOCK,
            "max": self.CURRENT_CLOCK_LIMIT,
            "boost": self.CURRENT_CLOCK_LIMIT
        }

        for setting, value in settings.items():
            with open("/sys/class/drm/card0/gt_{:s}_freq_mhz".format(setting), "w") as f:
                print("Setting clock level {:s} to {:d}".format(setting, value))
                f.write(str(value))

    def decide_action(self):
        # test criticals first
        if self.CURRENT_TEMP > self.CRITICAL_TEMP_LIMIT:
            return Action.THROTTLE_CRITICAL

        if self.CURRENT_TEMP > self.SAFE_TEMP_LIMIT:
            return Action.THROTTLE_MODERATE

        if self.CURRENT_TEMP < self.LOW_TEMP_LIMIT:
            return Action.BOOST_CRITICAL

        if self.CURRENT_TEMP < self.SAFE_TEMP_LIMIT:
            return Action.BOOST_MODERATE

        return Action.NO_OP