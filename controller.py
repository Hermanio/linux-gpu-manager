import dbus.service

from modes import StockGovernor, PowerSaveGovernor, PerformanceGovernor


class GPUManager(dbus.service.Object):

    def __init__(self, bus_name):
        super().__init__(bus_name, "/ee/ounapuu/GPUManager")

        self.CURRENT_GOVERNOR = None
        self.CURRENT_GOVERNOR_NAME = None
        self.CONTROLLER_MODES = ['powersave', 'normal', 'performance']

        self.start_governor('normal')

    @dbus.service.method("ee.ounapuu.GPUManager.setMode", in_signature='s', out_signature='s')
    def set_mode(self, mode):
        if mode in self.CONTROLLER_MODES:
            if mode == self.CURRENT_GOVERNOR_NAME:
                return "Mode already set to {:s}!".format(mode)
            else:
                self.stop_governor()
                self.start_governor(mode)
                return "Governor set to {:s}".format(mode)
        else:
            return "Invalid mode '{:s}'.".format(mode)

    def start_governor(self, mode):
        self.CURRENT_GOVERNOR = self.get_governor_by_name(mode)
        self.CURRENT_GOVERNOR_NAME = mode
        self.CURRENT_GOVERNOR.run_governor()

    def stop_governor(self):
        self.CURRENT_GOVERNOR.stop_governor()

    def get_governor_by_name(self, name):
        governors = {
            'normal': StockGovernor(),
            'powersave': PowerSaveGovernor(),
            'performance': PerformanceGovernor()
        }

        return governors[name]
