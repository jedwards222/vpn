#!/usr/bin/env python

#  
#  Adopted from Sergey's pytap example
#  Methods to create and configure a TUN interface in pure python. 
#

import os, sys
import fcntl
import struct

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000
TUNMODE = IFF_TUN       # Should set it to be TUN rather than TAP device
TUNSETOWNER = TUNSETIFF + 2

# Open TUN device file, create tun0
#
#  To open a new transient device, put "tun%d" into ioctl() below.
#   To open a persistent device, use "tun0" or the actual full name.
#
#  You can create a persistent device with "openvpn --mktun --dev tun0".
#   This device will show up on ifconfig, but will have "no link" unless  
#   it is opened by this or similar script even if you bring it up with
#   "ifconfig tun0 up". This can be confusing.
#
#   IFF_NO_PI is important! Otherwise, tap will add 4 extra bytes per packet, 
#     and this will confuse Scapy parsing.

def open(ifname = "tun0"):
    tun = os.open("/dev/net/tun", os.O_RDWR)
    ifs = fcntl.ioctl(tun, TUNSETIFF, struct.pack("16sH", ifname, TUNMODE | IFF_NO_PI))
    granted_ifname = ifs[:16].strip("\x00")  # will be tap0
    #  Optionally, we want tap0 be accessed by the normal user.
    fcntl.ioctl(tun, TUNSETOWNER, 1000)
    print "Allocated interface %s. Don't forget to configure it!" % granted_ifname
    return tun, granted_ifname
