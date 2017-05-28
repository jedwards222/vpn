#!/usr/bin/python

# VPN Server Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

# known port for VPN traffic
PORTNO = 8080

# VPN address of server.
# tunneled packets sent to this address will not be forwarded
MY_ADDR = '10.10.0.1'

# PSEUDOCODE
# 
# 1. setup_socket(port = 8080)
# 2. while (true)
# 3.    data = read_socket()
# 4.    if (data.len > 0)
# 5.    resp = parse_socket()
# 6.    send_resp(resp)
#
