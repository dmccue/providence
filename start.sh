#!/bin/bash
source .source

export PYTHONUNBUFFERED=1

SLACK_CMD='echo -e "$(date '+%Y\/%m\/%d_%H:%M:%S'):\n$(cat -)" | tee /dev/tty | slacker -c announce -n wifi-bot'

#git reset --hard HEAD && git pull


# Setup wifi monitor mode
sudo rfkill unblock wifi
sudo airmon-ng check kill
sudo airmon-ng start wlan0


# Start packet monitor
while pgrep -f python.*probe.py 2>&1 >/dev/null; do
  sudo pkill -f python.*probe.py 2>&1 >/dev/null
  sleep 2
done
sudo python -u probe.py -i wlan0mon 2>&1 >> data/probe.csv &


echo "Started watching files" | eval $SLACK_CMD
trap '{ sudo pkill -f python.*probe.py; echo "Stopped watching files" | eval $SLACK_CMD ; exit 1; }' INT

# Start file listener
inotifywait -m data |
  while read path action file; do
    #if [[ "$action" == "MOVED_TO" ]] && [[ "$file" =~ Kismet.*netxml$ ]]; then
    if [[ "$file" =~ probe.csv$  ]]; then
      ./alert.sh | slacker -c specific -n wifi-bot
    fi
  done
