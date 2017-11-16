#!/usr/bin/python

import time, datetime, argparse, netaddr, sys, logging
from scapy.all import *
from pprint import pprint
from logging.handlers import RotatingFileHandler

NAME = 'dsmprobe'
DESCRIPTION = "a command line tool for logging 802.11 probe request frames"

DEBUG = False

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
mac_cache = {}
ap_cache = {}
packetcounter = 0
counter = 0 
counter_interval = 60
event_warntimeout = 500
event_crittimeout = 600


def addAP( mac, packet ):
  if mac not in ap_cache.keys():
    epoch = int(time.time())
    print str(epoch) + ",newap," + mac + ',"' + packet.info.replace(',','.') + '",' + str(packet.type) + "," + str(packet.subtype)
    ap_cache[mac] = epoch

def addMAC( mac, packet ):
  if mac:
    epoch = int(time.time())
    if mac not in mac_cache.keys():
      print str(epoch) + ",newmac," + mac + ',"' + getManufacturer(mac).replace(',','.') + '",' + str(packet.type) + "," + str(packet.subtype)
      mac_cache[mac] = None
    if not mac_cache[mac]:
      print str(epoch) + ",eventUP," + mac + "," + str(packet.type) + "," + str(packet.subtype)
    mac_cache[mac] = epoch

def getManufacturer( mac ):
  try:
    parsed_mac = netaddr.EUI(mac)
    manufacturer = parsed_mac.oui.registration().org
  except netaddr.core.NotRegisteredError, e:
    return ""
  return manufacturer


def runStats():
  global packetcounter
  epoch = int(time.time())
  
  # Output stats
  try:
    print str(epoch) + ",stats," + str(len(mac_cache)) + "," + str(len(ap_cache)) + "," + str(packetcounter)
  except:
    pass

  # Output events
  for mac in mac_cache:
    if mac_cache[mac]:
      timediff = epoch - mac_cache[mac]
      if timediff >= event_warntimeout and timediff < event_crittimeout:
        print str(epoch) + ",eventWARN," + mac + "," + str(mac_cache[mac]) + "," + str(timediff)
      if timediff >= event_crittimeout:
        print str(epoch) + ",eventDOWN," + mac + "," + str(mac_cache[mac]) + "," + str(timediff) 
        mac_cache[mac] = None 


def build_packet_callback(logger):
  def packet_callback(packet):

    global counter
    global packetcounter 
  
    # Discard non 802.11 packets	
    if not packet.haslayer(Dot11):
      return

    packetcounter+=1
    
    # Get MACs
    macs = [ packet.addr1, packet.addr2, packet.addr3, packet.addr4 ]
    for mac in macs:
      addMAC(mac, packet)

    # Get APs
    if not hasattr(packet, 'info'):
      return

    if int(time.time()) - counter > counter_interval:
      counter = int(time.time())
      runStats() 

    if packet.type == 0:
      if packet.subtype in [ 0, 1, 5, 8, 11, 12, 13 ]:
        addAP(packet.addr3, packet)
        return
      if packet.subtype in [ 4 ]:
	# Mute subtype 4
        return

    print str(packet.type), str(packet.subtype), str(macs), packet.info

    return # returning from packet_callback
  return packet_callback # returning from build_packet_callback


def main():
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument('-i', '--interface', help="capture interface")
  parser.add_argument('-D', '--debug', action='store_true', help="enable debug output")
  args = parser.parse_args()

  if not args.interface:
    print "error: capture interface not given, try --help"
    sys.exit(-1)

  DEBUG = args.debug

  # setup our rotating logger
  #logger = logging.getLogger(NAME)
  #logger.setLevel(logging.INFO)
  #handler = RotatingFileHandler(args.output, maxBytes=args.max_bytes, backupCount=args.max_backups)
  #logger.addHandler(handler)
  #if args.log:
  #	logger.addHandler(logging.StreamHandler(sys.stdout))
  logger = ""
  built_packet_cb = build_packet_callback(logger)
  sniff(iface=args.interface, prn=built_packet_cb, store=0)

if __name__ == '__main__':
<<<<<<< HEAD
  main()
=======
  main()
>>>>>>> 118481ddab257e1a832cf9208000cedb2e8c53b5
