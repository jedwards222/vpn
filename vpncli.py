# VPN Client Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

# Imports
from scapy.all import * # scapy commands

import os       # for os.write, os.read

import pytun
import fakenet

# Set up tunnel (potentially see Sergey's pytab.open(tap0) - lines 15-17 of pong.py
# 1. Open tunnel

# 2. Configure tunnel interface


# Define any other helper functions


# Process packets going to the tunnel interface
while 1:
    # Get packet from kernel or from server connection that we need to modify/process


    # Check whether the packet we just read is from our own host, or from the server

    # If from Server:
       # Unwrap the packet

       # os.write it so the host machine's user can see the reply

    # If from Client:
        # Modify the packet before sending
    
        # Send the packet to the server
        
