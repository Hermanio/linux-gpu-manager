#!/bin/bash

#sudo python3 ../dbus-service.py &

#powersave
echo "powersave mode test"
python3 ../client powersave

#run tests with monitoring all data
MONITOR=all phoronix-test-suite benchmark pts/unigine-sanctuary

#cooldown
sleep 60

MONITOR=all phoronix-test-suite benchmark pts/nexuiz

#cooldown
sleep 60

MONITOR=all phoronix-test-suite benchmark pts/j2dbench

sleep 60


#normal
echo "normal mode test"
python3 ../client normal

#run tests with monitoring all data

MONITOR=all phoronix-test-suite benchmark pts/unigine-sanctuary

#cooldown
sleep 60

MONITOR=all phoronix-test-suite benchmark pts/nexuiz

#cooldown
sleep 60

phoronix-test-suite benchmark pts/j2dbench

sleep 60


#performance
echo "performance mode test"
python3 ../client performance

#run tests with monitoring all data

MONITOR=all phoronix-test-suite benchmark pts/unigine-sanctuary

#cooldown
sleep 60

MONITOR=all phoronix-test-suite benchmark pts/nexuiz


#cooldown
sleep 60

MONITOR=all phoronix-test-suite benchmark pts/j2dbench

sleep 60

