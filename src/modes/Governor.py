# Copyright (C) 2018 Herman Õunapuu
#
# This file is part of Linux GPU Manager.
#
# Linux GPU Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux GPU Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux GPU Manager.  If not, see <http://www.gnu.org/licenses/>.


import multiprocessing
from abc import ABCMeta, abstractmethod


class Governor(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Init shared components.
        Other governors may want to use multiple temperature levels or different MHz steppings
        or aggressive polling, thus we don't set these here.

        First time run stuff can also be initialised in run_governor method.
        :param name:
        """
        self.governor_name = None
        self.default_min_clock = None
        self.default_stock_clock = None
        self.default_max_clock = None

        self.current_clock_limit = None
        self.current_temperature = None

        self.governor_thread = None

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
        self.governor_thread = multiprocessing.Process(target=self.start)
        self.governor_thread.start()

    def stop_governor(self):
        """
        Stops the governor main loop from running.
        :return:
        """
        print("Stopping governor {:s}...".format(self.governor_name))
        self.governor_thread.terminate()
        self.governor_thread = None

    def read_temps(self):
        """
        Reads GPU temp (if not available, read package temp/CPU temp).
        If over limit, throttle clock.
        :return:
        """
        # todo enumerate paths, collect all temps, then get max
        temp_path = "/sys/class/thermal/thermal_zone1/temp"

        # todo handle IO error
        with open(temp_path, "r") as f:
            self.current_temperature = int(f.read()) / 1000

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
                    self.default_min_clock = clockspeed
                elif level == "max":
                    self.default_stock_clock = clockspeed
                elif level == "boost":
                    self.default_max_clock = clockspeed

        self.current_clock_limit = self.default_min_clock
