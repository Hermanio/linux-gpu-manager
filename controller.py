import dbus.service

from modes import StockGovernor, PowerSaveGovernor, PerformanceGovernor


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
