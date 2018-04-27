import time

from modes.Action import Action
from modes.Governor import Governor


class StockGovernor(Governor):
    """
    Runs the GPU at specified "max" clock speed (stock).
    """

    def __init__(self):
        super().__init__()
        self.governor_name = "STOCK_GOVERNOR"

        self.low_temp_limit = 70
        self.safe_temp_limit = 90
        self.critical_temp_limit = 95

        # Intel HD4000 has 50MHZ steppings, setting them will automatically
        self.small_mhz_stepping = 50
        self.big_mhz_stepping = 200

        self.governor_poll_period_in_seconds = 1.0

    def start(self):
        """
        Starts the governor main loop.
        :return:
        """

        print("Starting governor {:s}...".format(self.governor_name))

        # main loop
        while True:
            self.read_temps()

            # get action
            action = self.decide_action()

            # apply action
            self.apply_action(action)

            # print status
            # self.get_status()

            # sleep... I need some, too
            time.sleep(self.governor_poll_period_in_seconds)

    def apply_action(self, action):
        """
        Apply settings.
        :param min:
        :param stock:
        :param max:
        :return:
        """
        if action == Action.THROTTLE_MODERATE:
            clock_change = -self.small_mhz_stepping
        elif action == Action.THROTTLE_CRITICAL:
            clock_change = -self.big_mhz_stepping
        elif action == Action.BOOST_MODERATE:
            clock_change = self.small_mhz_stepping
        elif action == Action.BOOST_CRITICAL:
            clock_change = self.big_mhz_stepping
        elif action == Action.NO_OP:
            clock_change = 0
        else:
            clock_change = 0

        self.current_clock_limit = self.current_clock_limit + clock_change

        if self.current_clock_limit < self.default_min_clock:
            self.current_clock_limit = self.default_min_clock

        if self.current_clock_limit > self.default_stock_clock:
            self.current_clock_limit = self.default_stock_clock

        # min, max, boost
        settings = {
            "min": self.default_min_clock,
            "max": self.current_clock_limit,
            "boost": self.current_clock_limit
        }

        for setting, value in settings.items():
            with open("/sys/class/drm/card0/gt_{:s}_freq_mhz".format(setting), "w") as f:
                print("Setting clock level {:s} to {:d}".format(setting, value))
                f.write(str(value))

    def decide_action(self):
        # test criticals first
        if self.current_temperature > self.critical_temp_limit:
            return Action.THROTTLE_CRITICAL

        if self.current_temperature > self.safe_temp_limit:
            return Action.THROTTLE_MODERATE

        if self.current_temperature < self.low_temp_limit:
            return Action.BOOST_CRITICAL

        if self.current_temperature < self.safe_temp_limit:
            return Action.BOOST_MODERATE

        return Action.NO_OP
