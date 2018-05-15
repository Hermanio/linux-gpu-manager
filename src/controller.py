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


import dbus.service

from modes.PerformanceGovernor import PerformanceGovernor
from modes.PowerSaveGovernor import PowerSaveGovernor
from modes.StockGovernor import StockGovernor


class GPUManager(dbus.service.Object):

    def __init__(self, bus_name):
        super().__init__(bus_name, "/ee/ounapuu/GPUManager")

        self.current_governor = None
        self.current_governor_name = None
        self.controller_modes = ['powersave', 'normal', 'performance']

        self.start_governor('normal')

    @dbus.service.method("ee.ounapuu.GPUManager.setMode", in_signature='s', out_signature='s')
    def set_mode(self, mode):
        if mode in self.controller_modes:
            if mode == self.current_governor_name:
                return "Mode already set to {:s}!".format(mode)
            else:
                self.stop_governor()
                self.start_governor(mode)
                return "Governor set to {:s}".format(mode)
        else:
            return "Invalid mode '{:s}'.".format(mode)

    def start_governor(self, mode):
        self.current_governor = self.get_governor_by_name(mode)
        self.current_governor_name = mode
        self.current_governor.run_governor()

    def stop_governor(self):
        self.current_governor.stop_governor()

    def get_governor_by_name(self, name):
        governors = {
            'normal': StockGovernor(),
            'powersave': PowerSaveGovernor(),
            'performance': PerformanceGovernor()
        }

        return governors[name]
