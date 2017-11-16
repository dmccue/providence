#!/bin/bash


source .source
SLACK_CMD='echo -e "$(date '+%Y\/%m\/%d_%H:%M:%S'):\n$(cat -)" | tee /dev/tty | slacker -c announce -n wifi-bot'

echo "Started watching files" | eval $SLACK_CMD
trap '{ echo "Stopped watching files" | eval $SLACK_CMD ; exit 1; }' INT

inotifywait -m data |
    while read path action file; do
        #if [[ "$action" == "MOVED_TO" ]] && [[ "$file" =~ Kismet.*netxml$ ]]; then
          # If change to Kismet xml logfile
          #echo "File updated $file" && python wifi-format.py "data/$file" && \
          #echo "File updated $file" && python wifi-process.py | tee -a data/wifi-process.log | eval $SLACK_CMD && /
        if [[ "$file" =~ dsmprobe.csv$  ]]; then

          ./alert.sh | slacker -c specific -n wifi-bot

        fi

    done
