#!/usr/bin/python
import json, time, datetime


try:
  with open("data/probe.csv") as f:
    lines = f.readlines()
except ValueError:
    lines = []

macs = {}
events = []

for line in lines:
  lineArray = line.strip("\n").split(",")
  if not lineArray[2] in macs.keys():
    if lineArray[1].startswith('eventUP') or lineArray[1].startswith('eventDOWN'):
      macs[lineArray[2]] = []
  else:
    if lineArray[1].startswith('eventUP'):
      macs[lineArray[2]].append(lineArray[0]+"u")
    elif lineArray[1].startswith('eventDOWN'):
      macs[lineArray[2]].append(lineArray[3]+"d")

#print "Finished load..."

for mac in macs.keys():
  if len(macs[mac]) > 3:
    macs[mac].sort()
    #print mac, str(len(macs[mac])), macs[mac]
    timeUP = None
    timeDOWN = None
    for event in macs[mac]:
      if event.endswith('u'):
        timeUP = int(event.strip('u'))
      if event.endswith('d') and timeUP and int(event.strip('d')) > timeUP:
        timeDOWN = int(event.strip('d'))
      if timeUP and timeDOWN and timeDOWN > timeUP:
        #print "Event", time.strftime("%H:%M:%S", time.gmtime(timeUP)), time.strftime("%H:%M:%S", time.gmtime(timeDOWN)), (timeDOWN-timeUP)
        #print "Event", timeUP, timeDOWN, (timeDOWN-timeUP)
        #events.append([mac,datetime.datetime.fromtimestamp(timeUP),datetime.datetime.fromtimestamp(timeDOWN)])
        events.append([mac, timeUP, timeDOWN])
        timeUP, timeDOWN = None, None

print str(events)
