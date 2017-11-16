#!/bin/bash
export PYTHONUNBUFFERED=1

sudo airmon-ng check kill
sudo airmon-ng start wlan0

git reset --hard HEAD && git pull

pgrep providence-monitor.sh 2>&1 >/dev/null \
  && pkill providence-monitor.sh
./providence-monitor.sh 2>&1 > data/providence-monitor.log
sudo python -u probe.py -i wlan0mon | tee -a data/probe.csv
