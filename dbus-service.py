#!/usr/bin/env python3
#implementation plan
# read sensor data (if not available, use coretemp as indicator)

#API

#set-mode :
# powersave always at lowest clocks
# normal non-OC perf
# max performance max-OC perf

# if max temp is reached, employ thermal daemon style throttle
import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

# Initialize a main loop
DBusGMainLoop(set_as_default=True)
loop = GLib.MainLoop()

# Declare a name where our service can be reached
try:
    bus_name = dbus.service.BusName("ee.ounapuu.GPUManager",
                                    bus=dbus.SystemBus(),
                                    do_not_queue=True)
except dbus.exceptions.NameExistsException:
    print("service is already running")
    sys.exit(1)

# Run the loop
try:
    # Create our initial objects
    from controller import GPUController

    GPUController(bus_name)

    loop.run()
except KeyboardInterrupt:
    print("keyboard interrupt received")
except Exception as e:
    print("Unexpected exception occurred: '{}'".format(str(e)))
finally:
    loop.quit()
