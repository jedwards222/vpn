#!/usr/bin/env python

#
#  Configuration for our VPN tunnel interface
#  Code adopted from Sergey's example
#

import subprocess
import re           # for matching out MAC
import pytun

#
#   This interface will be the "gateway" into the fake network
#    NOTE: check if other routes for this network exist, warn & exit if so!
#
GW_MAC   = '02:02:03:04:05:01' # multicast bit: off, locally-administered bit: on
BASE_MAC = '02:02:03:04:05:'   #  same, less last byte

def configure_iface(ifname, ether, ip, netmask = '255.255.255.0', bcast = ''):
    # Bring it down first
    subprocess.check_call("ifconfig %s down" % ifname, shell=True)

    hw_cfg_cmd = "ifconfig %s hw ether %s " % (ifname, ether)
    # Something causes this to fail on MacOS:
    try:
      subprocess.check_call( hw_cfg_cmd, shell=True)
    except:
      print "%s seems unsupported on this platform, skipping\n" % hw_cfg_cmd
      pass

    if bcast != '':
      ip_cfg_cmd = "ifconfig %s %s netmask %s broadcast %s up" % (ifname, ip, netmask, bcast)
    else:
      # ...and hope ifconfig is smart and computes bcast address! YMMV.
      ip_cfg_cmd = "ifconfig %s %s netmask %s up" % (ifname, ip, netmask)

    subprocess.check_call( ip_cfg_cmd, shell=True)

#  Configure given tap device to be on the fake network
def configure_tun(ifname, gw_ip):
    configure_iface(ifname, GW_MAC, gw_ip)
