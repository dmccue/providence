#!/bin/bash
export PYTHONUNBUFFERED=1

sudo airmon-ng check kill
sudo airmon-ng start wlan0

git reset --hard HEAD && git pull

pgrep providence-monitor.sh 2>&1 >/dev/null || \
  ./providence-monitor.sh 2>&1 | tee -a data/providence-monitor.log
sudo python -u probe.py -i wlan0mon | tee -a data/probe.csv
