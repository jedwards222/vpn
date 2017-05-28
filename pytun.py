#!/usr/bin/env python

#
#  Methods to create and configure a TUN interface in pure python. 
#

import os, sys
import fcntl
import struct

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000
TUNMODE = IFF_TAP
TUNSETOWNER = TUNSETIFF + 2

# Open TUN device file, create tap0
#
#  To open a new transient device, put "tap%d" into ioctl() below.
#   To open a persistent device, use "tap0" or the actual full name.
#
#  You can create a persistent device with "openvpn --mktun --dev tap0".
#   This device will show up on ifconfig, but will have "no link" unless  
#   it is opened by this or similar script even if you bring it up with
#   "ifconfig tap0 up". This can be confusing.
#
#  Copied from https://gist.github.com/glacjay/585369 
#   IFF_NO_PI is important! Otherwise, tap will add 4 extra bytes per packet, 
#     and this will confuse Scapy parsing.

def open(ifname = "tap0"):
    tun = os.open("/dev/net/tun", os.O_RDWR)
    ifs = fcntl.ioctl(tun, TUNSETIFF, struct.pack("16sH", ifname, TUNMODE | IFF_NO_PI))
    granted_ifname = ifs[:16].strip("\x00")  # will be tap0
    #  Optionally, we want tap0 be accessed by the normal user.
    fcntl.ioctl(tun, TUNSETOWNER, 1000)
    print "Allocated interface %s. Don't forget to configure it!" % granted_ifname
    return tun, granted_ifname
