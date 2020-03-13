#!/bin/bash

cd /home/pi/scada-nogit/services/systemd_files

cp data_sorter.service /etc/systemd/system
cp data_calibrator.service /etc/systemd/system

systemctl start data_sorter
systemctl start data_calibrator

systemctl daemon-reload

# copy bash-utils into path


