#!/bin/bash

# Set up tun interface
echo "Setting up tun0 interface"
openvpn --mktun --dev tun0
echo "Completed setting up interface"
