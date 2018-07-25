#!/usr/bin/env bash

sudo cp ./conf/ee.ounapuu.GPUManager.conf /etc/dbus-1/system.d/

sudo mkdir -p /usr/bin/linux-gpu-manager
sudo cp -a ./src/. /usr/bin/linux-gpu-manager/
sudo chmod +x /usr/bin/linux-gpu-manager/client
sudo chmod +x /usr/bin/linux-gpu-manager/service

sudo cp ./conf/linux-gpu-manager.service /etc/systemd/system/
sudo systemctl enable linux-gpu-manager.service