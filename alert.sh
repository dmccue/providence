#!/bin/bash

file=${1:-"data/probe.csv"}

# Get previous linecount
prevlinecount=$(cat $file.count 2>/dev/null)
prevlinecount=${prevlinecount:-"0"}

# Get current linecount
curlinecount=$(wc -l $file | cut -d' ' -f1)


if [[ "$curlinecount" -gt "$prevlinecount" ]]; then
  # Additional lines
  prevlinecountplusone=$(( prevlinecount + 1 ))
  additionlines=$(sed -n ${prevlinecountplusone},${curlinecount}p $file)
fi

if [[ "$curlinecount" -lt "$prevlinecount" ]]; then
  #Reset
  additionlines=$(sed -n 1,${curlinecount}p $file)
fi


output=""
results=$(echo "${additionlines}" | grep -i -e ",eventUP," -e ",eventDOWN,")
for i in $(cat data/maclookup.csv | grep -v '^#' | cut -d, -f1); do
  match=$(echo "$results" | grep -i "$i")
  if [[ "$match" ]]; then
    description=$(cat data/maclookup.csv | grep -v '^#' | grep -i "$i" | cut -d, -f2)
    convertedtime=$(echo "$match" | cut -d, -f1 | { read stdin; date -d "@$stdin" +%H:%M:%S;} )
    #description=""
    if [[ $description =~ .*,eventDOWN,.* ]]; then
      convertedtime=$(echo "$match" | cut -d, -f4 | { read stdin; date -d "@$stdin" +%H:%M:%S;} )
    fi
    output="$output$match,$convertedtime,$description\n"
  fi
done


if [[ "$output" ]]; then
  echo -e "$output"
fi

echo "$curlinecount" > $file.count
