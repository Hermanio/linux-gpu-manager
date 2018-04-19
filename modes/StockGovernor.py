import sys
import time

from modes.Action import Action


class StockGovernor(object):
    """
    Runs the GPU at specified "max" clock speed (stock).
    """

    def __init__(self):
        self.DEFAULT_MIN_CLOCK = None
        self.DEFAULT_STOCK_CLOCK = None
        self.DEFAULT_MAX_CLOCK = None

        self.CURRENT_CLOCK_LIMIT = None
        self.CURRENT_TEMP = None

        self.GOVERNOR_RUNNING = True

        self.GOVERNOR_NAME = "STOCK_GOVERNOR"

        self.LOW_TEMP_LIMIT = 70
        self.SAFE_TEMP_LIMIT = 80
        self.CRITICAL_TEMP_LIMIT = 90

        # Intel HD4000 has 50MHZ steppings, setting them will automatically
        self.SMALL_MHZ_STEPPING = 50
        self.BIG_MHZ_STEPPING = 200

        self.GOVERNOR_POLL_PERIOD_IN_SECONDS = 1.0

    def run_governor(self):
        """
        Starts the governor main loop.
        :return:
        """
        print("Starting governor {:s}...".format(self.GOVERNOR_NAME))

        # detection, initial temps
        self.read_spec_mhz()
        self.read_temps()

        # main loop
        while self.GOVERNOR_RUNNING:
            # read temps
            self.read_temps()

            # get action
            action = self.decide_action()

            # apply action
            self.apply_action(action)

            # print status
            self.get_status()

            # sleep... I need some, too
            time.sleep(self.GOVERNOR_POLL_PERIOD_IN_SECONDS)

        print("Stopping governor {:s}...".format(self.GOVERNOR_NAME))

    def get_status(self):
        """
        Returns the current state (package temp, min med max clocks, current clock)
        :return:
        """
        stats = {
            "Current freq": "gt_cur_freq_mhz",
            "Actual freq": "gt_act_freq_mhz",
            "Maximum freq": "gt_max_freq_mhz",
            "Minimum freq": "gt_min_freq_mhz",
            "Boost freq": "gt_boost_freq_mhz",
            "SPEC max freq": "gt_RP0_freq_mhz",
            "SPEC normal freq": "gt_RP1_freq_mhz",
            "SPEC min freq": "gt_RPn_freq_mhz",
        }

        for stat, path in stats.items():
            with open("/sys/class/drm/card0/{:s}".format(path)) as f:
                print("{:s}:\t{:s}".format(stat, f.read()), end='')
        print()

    def apply_action(self, action):
        """
        Apply settings.
        :param min:
        :param stock:
        :param max:
        :return:
        """
        clock_change = None
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

        if self.CURRENT_CLOCK_LIMIT > self.DEFAULT_STOCK_CLOCK:
            self.CURRENT_CLOCK_LIMIT = self.DEFAULT_STOCK_CLOCK

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

    def stop_governor(self):
        """
        Stops the governor.
        :return:
        """
        self.GOVERNOR_RUNNING = False

    def decide_action(self, ):
        """
        Takes into account current clock, low-normal-high and makes decision
        :return:
        """
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

    def read_temps(self):
        """
        Reads GPU temp (if not available, read package temp/CPU temp).
        If over limit, throttle clock.
        :return:
        """
        # todo enumerate paths, collect all temps, then get max
        TEMP_PATH = "/sys/class/thermal/thermal_zone1/temp"

        # todo handle IO error
        with open(TEMP_PATH, "r") as f:
            self.CURRENT_TEMP = int(f.read()) / 1000

    def read_spec_mhz(self):
        paths = {
            "boost": "gt_RP0_freq_mhz",
            "max": "gt_RP1_freq_mhz",
            "min": "gt_RPn_freq_mhz",
        }
        for level, path in paths.items():
            with open("/sys/class/drm/card0/{:s}".format(path)) as f:
                clockspeed = int(f.read())
                if level == "min":
                    self.DEFAULT_MIN_CLOCK = clockspeed
                elif level == "max":
                    self.DEFAULT_STOCK_CLOCK = clockspeed
                elif level == "boost":
                    self.DEFAULT_MAX_CLOCK = clockspeed

        self.CURRENT_CLOCK_LIMIT = self.DEFAULT_MIN_CLOCK
