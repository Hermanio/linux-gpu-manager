import multiprocessing
from abc import ABCMeta, abstractmethod


class Governor(object):
    __metaclass__ = ABCMeta

    def __init__(self, name):
        """
        Init shared components.
        Other governors may want to use multiple temperature levels or different MHz steppings
        or aggressive polling, thus we don't set these here.

        First time run stuff can also be initialised in run_governor method.
        :param name:
        """
        self.DEFAULT_MIN_CLOCK = None
        self.DEFAULT_STOCK_CLOCK = None
        self.DEFAULT_MAX_CLOCK = None

        self.CURRENT_CLOCK_LIMIT = None
        self.CURRENT_TEMP = None

        self.GOVERNOR_NAME = name

        self.GOVERNOR_THREAD = None

        self.read_spec_mhz()
        self.read_temps()

    @abstractmethod
    def start(self):
        """
        Method containing main loop. Gets called via multiprocess API.
        :return:
        """
        pass

    @abstractmethod
    def apply_action(self, action):
        """
        Apply the given action.
        :param action:
        :return:
        """
        pass

    @abstractmethod
    def decide_action(self):
        """
        Takes into account current clock, low-normal-high and makes decision
        :return:
        """
        pass

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

    def run_governor(self):
        """
        Starts the governor process.
        """
        self.GOVERNOR_THREAD = multiprocessing.Process(target=self.start)
        self.GOVERNOR_THREAD.start()

    def stop_governor(self):
        """
        Stops the governor main loop from running.
        :return:
        """
        print("Stopping governor {:s}...".format(self.GOVERNOR_NAME))
        self.GOVERNOR_THREAD.terminate()
        self.GOVERNOR_THREAD = None

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
