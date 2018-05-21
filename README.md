# linux-gpu-manager
Linux GPU Manager is a service that allows to control GPU performance range to achieve better power savings and prevent overheating.

Currently supports Intel GPU-s. Work in progress.

# How to run

This should run on any recent distribution, such as Ubuntu 18.04 and Arch Linux. 

1. Deploy the dbus config file:
`sudo bash deploy-dbus-conf.sh`

2. Start the GPU manager service:
`sudo python3 src/dbus-service.py`

3. To change the governor, run 
`python3 src/client 'governor-name-here'`. 
Example of setting the governor to powersave mode: 
`python3 src/client powersave`

Available governors: powersave, normal, performance
