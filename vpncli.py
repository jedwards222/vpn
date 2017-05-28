# VPN Client Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

# Imports
from scapy.all import * # scapy commands

import os       # for os.write, os.read

import pytun
import fakenet

import socket   # for socket.socket, socket.connect

iname = 'tun0'

#check to see if a tun iface exists
ifacelist = os.listdir('/sys/class/net/')
if not(iname in ifacelist):
    print "please create a tun0 interface using openvpn"


'''
Set up tunnel - based on Sergey's pong.py
'''
# 1. Open tunnel
tun, ifname = pytun.open('tun0')
# 2. Configure tunnel interface
print "Allocated interface %s. Configuring it." % ifname
fakenet.configure_tap(ifname)

'''
Set up connection to the VPN server
'''
# Create Socket
socket_family = AF_INET
socket_type = SOCK_STREAM
s = socket.socket (socket_family, socket_type, protocol=0)
# Connect to server
hostname = "flume.cs.dartmouth.edu"
port = 8080
s.connect(hostname, port)

'''
Process packets going to the tunnel interface
'''
rlist = [tun,s]

while 1:
    readable, writable, exceptional = select.select(rlist, [], [])
    for r in readable:
        if r == tun:        # Packet is from host, so send it
            binary_packet = os.read(tun, 2048)
            s.send(binary_packet)
        if r == s:          # Packet is from server, so pass on to host
            data = s.recv(2048)
            os.write(tun,IP(data))


# Close the socket connection when exiting - this should maybe go elsewhere
s.close
