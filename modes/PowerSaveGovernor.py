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
