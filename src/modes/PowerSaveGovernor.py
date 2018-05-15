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


import time

from modes.Governor import Governor


class PowerSaveGovernor(Governor):
    """
    Runs the GPU at specified min clock speed at all times.
    """

    def __init__(self, ):
        super().__init__()
        self.governor_name = "POWERSAVE_GOVERNOR"

        self.governor_poll_period_in_seconds = 5.0

    def start(self):
        print("Starting governor {:s}...".format(self.governor_name))
        # main loop
        while True:
            self.read_temps()

            self.apply_action()
            time.sleep(self.governor_poll_period_in_seconds)

    def apply_action(self, action=None):
        # min, max, boost
        settings = {
            "min": self.default_min_clock,
            "max": self.default_min_clock,
            "boost": self.default_min_clock
        }

        for setting, value in settings.items():
            with open("/sys/class/drm/card0/gt_{:s}_freq_mhz".format(setting), "w") as f:
                print("Setting clock level {:s} to {:d}".format(setting, value))
                f.write(str(value))

    def decide_action(self):
        pass
