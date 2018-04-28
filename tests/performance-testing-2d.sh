echo "powersave mode test"
python3 ../client powersave

#run tests with monitoring all data
MONITOR=all phoronix-test-suite benchmark pts/j2dbench

sleep 60

echo "normal mode test"
python3 ../client normal

#run tests with monitoring all data
MONITOR=all phoronix-test-suite benchmark pts/j2dbench

sleep 60

echo "performance mode test"
python3 ../client performance

#run tests with monitoring all data
MONITOR=all phoronix-test-suite benchmark pts/j2dbench

sleep 60

