import time

from modes.Governor import Governor


class PowerSaveGovernor(Governor):
    """
    Runs the GPU at specified min clock speed at all times.
    """

    def __init__(self, ):
        super().__init__()
        self.GOVERNOR_NAME = "POWERSAVE_GOVERNOR"

        self.GOVERNOR_POLL_PERIOD_IN_SECONDS = 5.0

    def start(self):
        print("Starting governor {:s}...".format(self.GOVERNOR_NAME))
        # main loop
        while True:
            self.apply_action()
            time.sleep(self.GOVERNOR_POLL_PERIOD_IN_SECONDS)

    def apply_action(self, action=None):
        # min, max, boost
        settings = {
            "min": self.DEFAULT_MIN_CLOCK,
            "max": self.DEFAULT_MIN_CLOCK,
            "boost": self.DEFAULT_MIN_CLOCK
        }

        for setting, value in settings.items():
            with open("/sys/class/drm/card0/gt_{:s}_freq_mhz".format(setting), "w") as f:
                print("Setting clock level {:s} to {:d}".format(setting, value))
                f.write(str(value))

    def decide_action(self):
        pass
