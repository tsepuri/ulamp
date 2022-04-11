#!/bin/bash

cd ~/connected-devices/Lampi/pkg/
cp ../main.py lampi/opt/lampi/lamp_ui.py
cp ../lamp_service.py lampi/opt/lampi
cp ../bluetooth/peripheral.js lampi/opt/lampi/bluetooth/bt_peripheral.js
cp -r ../lampi lampi/opt/lampi
cp -r ../images lampi/opt/lampi
cp ../lamp_common.py lampi/opt/lampi
bumpversion minor
dpkg-deb --build lampi
reprepro -b ~/connected-devices/Web/reprepro/ubuntu/ includedeb lampi lampi.deb
