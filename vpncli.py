# VPN Client Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

# Imports
from scapy.all import * # scapy commands

import os       # for os.write, os.read

import pytun
import fakenet


#function to swap ip src and dst
def swap_src_and_dst(pkt, layer):
  pkt[layer].dst, pkt[layer].src = pkt[layer].src, pkt[layer].dst


iname = 'tun0'

#check to see if a tun iface exists
ifacelist = os.listdir('/sys/class/net/')
if not(iname in ifacelist):
    print "please create a tun0 interface using openvpn"


# Set up tunnel (potentially see Sergey's pytab.open(tap0) - lines 15-17 of pong.py
# 1. Open tunnel
tun, ifname = pytun.open('tun0')
# 2. Configure tunnel interface
print "Allocated interface %s. Configuring it." % ifname
fakenet.configure_tap(ifname)



# Define any other helper functions


# Process packets going to the tunnel interface
while 1:

    # Get packet from kernel or from server connection that we need to modify/process
    binary_packet = os.read(tun, )



    # Check whether the packet we just read is from our own host, or from the server

    # If from Server:
       # Unwrap the packet

       # os.write it so the host machine's user can see the reply

    # If from Client:
        # Modify the packet before sending
    
        # Send the packet to the server
        
