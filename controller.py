import getpass
import multiprocessing
import re

import dbus.service

from modes.StockGovernor import StockGovernor


class GPUController(dbus.service.Object):
    CONTROLLER_MODES = ['powersave', 'normal', 'performance']

    CURRENT_GOVERNOR = None

    def __init__(self, bus_name):
        super().__init__(bus_name, "/ee/ounapuu/GPUManager")
        self.start_default_governor()

    @dbus.service.method("ee.ounapuu.GPUManager.setMode", in_signature='s', out_signature='s')
    def set_mode(self, mode):
        return "set mode {:s}".format(mode)

    def start_default_governor(self):
        self.CURRENT_GOVERNOR = StockGovernor()
        self.CURRENT_GOVERNOR.run_governor()
