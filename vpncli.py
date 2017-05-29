# VPN Client Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

from scapy.all import * # scapy commands
import os               # os.write, os.read
import pytun            # pytun.open
import fakenet          # fakenet.configure_tun
import socket           # socket.socket, socket.connect
import select
# import struct           

HOSTNAME = 'wolfe.cloudapp.net'         # Willy Wolfe's Azure Server
# HOSTNAME = 'flume.cs.dartmouth.edu'   # Flume
PORT = 5000

# Check to see if a tun iface exists
iname = 'tun0'
ifacelist = os.listdir('/sys/class/net/')
if not(iname in ifacelist):
    print("please create a tun0 interface using openvpn")

#######################################
# Set up connection to the VPN server #
#######################################
# Create Socket
socket_family = socket.AF_INET
socket_type = socket.SOCK_STREAM
s = socket.socket (socket_family, socket_type, 0)
# Connect to server
print("----\nConnecting to " + HOSTNAME + ":" + str(PORT))
s.connect((HOSTNAME, PORT))
print("Connected\n----")
# Server will send your IP address
newip = s.recv(2048)
print("Your VPN IP Address: " + socket.inet_ntop(socket.AF_INET,newip))
gw_ip = (socket.inet_ntop(socket.AF_INET,newip))

#############################################
# Set up tunnel - based on Sergey's pong.py #
#############################################
# 1. Open tunnel
tun, ifname = pytun.open('tun0')
# 2. Configure tunnel interface
print ("Allocated interface " + str(ifname) + ". Configuring it.")
fakenet.configure_tun(ifname, gw_ip)

#################################################
# Process packets going to the tunnel interface #
#################################################
rlist = [tun,s]
while 1:
    readable, writable, exceptional = select.select(rlist, [], [])
    for r in readable:
        if r == tun:        # Packet is from host, so send it
            binary_packet = os.read(tun, 2048)
            s.send(binary_packet)
        if r == s:          # Packet is from server, so pass on to host
            data = s.recv(2048)
            os.write(tun,str(IP(data)))

# Close the socket connection when exiting - this should maybe go elsewhere
s.close
