#!/usr/bin/python

# VPN Server Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

import socket
import select
import struct
from scapy.all import *

HOST = ''    # symbolic name meaning all available interfaces
PORT = 8080  # known port for VPN traffic
BKLG = 5     # length of backlog for pending connections on socket

# VPN address of server.
# tunneled packets sent to this address will not be forwarded
MY_ADDR    = '10.10.0.1'
NET_PREFIX = '10.10.0.'

# for convenience
IP_MAXPACKET = 65535

def main():
    server_socket = init_tcp_socket() # init socket, set to listen
    read_list = [server_socket]       # list of open sockets
    client_dict = {}                  # dict mapping fileno:local_addr_string
    avail = 2
    while True: # loop indefinitely
        # wait for incoming packet on any connection
        readable, writable, errored = select.select(read_list, [], [])
        for sock in readable:
            if sock == server_socket: # new connection
                client_socket, address = server_socket.accept() # accept
                read_list.append(client_socket)                 # add to list
                # set up a VM address associated with this client connection
                client_addr, avail = client_setup(address, avail, sock)
                client_dict[client_addr] = client_socket.fileno()                
            else:
                data = sock.recv(IP_MAXPACKET) # get packet from client 
                if data:
                    process_packet(data, client_dict, client_socket): # handle packet     
                else: 
                    del client_dict[sock] # remove from client dict
                    sock.close()                   # close this connection
                    read_list.remove(sock)         # remove from read_list

def init_tcp_socket(port=PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # create socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # skip timeout
    sock.bind((HOST, port))                                    # bind to port
    sock.listen(BKLG)                                          # set to listen
    print "server_socket listening on port %d" % port
    return sock

def client_setup(address, avail, sock):
    client_addr = NET_PREFIX + str(avail)
    sock.send(socket.htonl(socket.inet_pton(AF_INET, client_addr)))
    return client_addr, avail+1

def process_packet(data, client_dict, client_socket):
    packet = IP(data)
    dst_addr = packet[IP].dst
    for addr in client_dict.keys():
        if addr == dst_addr:
            if addr == MY_ADDR:
                handle_ping(data, client_socket)
            else:
                route_packet(data, client_dict[addr])

def handle_ping(data, client_socket):
    packet = IP(data)
    if packet.haslayer(ICMP) and packet[ICMP] == 8:
        pong = packet.copy()
        swap_src_and_dst(pong, IP)
        pong[ICMP].type='echo-reply'
        pong[ICMP].chksum = None   # force recalculation
        pong[IP].chksum   = None
        client_socket.send(pong.build())

def route_packet(data, socket):
    socket.send(data)          

if __name__ == "__main__":
    main()
