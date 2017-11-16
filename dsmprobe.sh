#!/bin/bash

export PYTHONUNBUFFERED=1

if [ ! -d "$DIRECTORY" ]; then
  git clone https://gist.github.com/a075175705f0f7abaed34b1018ecd1f5.git dsmprobe
fi
cd dsmprobe && git reset --hard HEAD && git pull && cd .. && ln -sf dsmprobe/dsmprobe.py dsmprobe.py 
sudo python -u dsmprobe.py -i wlan0mon | tee -a data/dsmprobe.csv
