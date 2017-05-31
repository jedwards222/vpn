#!/usr/bin/python

# VPN Server Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

import socket
import select
import struct
import scapy.all
import encryption   # encrypt and decrypt

HOST = ''    # symbolic name meaning all available interfaces
PORT = 5000  # known port for VPN traffic
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
    sock2addr = {server_socket.fileno():MY_ADDR} # dict, fileno:addr_string
    addr2sock = {MY_ADDR:server_socket}          # dict, addr_string:fileno
    avail = 2
    while True: # loop indefinitely
        # wait for incoming packet on any connection
        readable, writable, errored = select.select(read_list, [], [])
        for sock in readable:
            if sock == server_socket: # new connection
                client_socket, address = server_socket.accept() # accept
                read_list.append(client_socket)                 # add to list
                # set up a VM address associated with this client connection
                client_addr, avail = client_setup(avail, client_socket)
                sock2addr[client_socket.fileno()] = client_addr
                addr2sock[client_addr] = client_socket
                print "new connection on socket %d, assigning addr %s" % (
                        client_socket.fileno(), client_addr
                      )
            else:
                data = sock.recv(IP_MAXPACKET) # get packet from client
                if data:
                    print "got packet from %s" % sock2addr[sock.fileno()]
                    process_packet(data, sock2addr, addr2sock, sock)
                else:
                    print "closing connection w/ %s" % sock2addr[sock.fileno()]
                    # remove from maps
                    addr = sock2addr[sock.fileno()]
                    del sock2addr[sock.fileno()]
                    del addr2sock[addr]                    
                    sock.close()            # close this connection
                    read_list.remove(sock)  # remove from read_list

def init_tcp_socket(port=PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # create socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # skip timeout
    sock.bind((HOST, port))                                    # bind to port
    sock.listen(BKLG)                                          # set to listen
    print "server_socket listening on port %d" % port
    return sock

def client_setup(avail, sock):
    client_addr = NET_PREFIX + str(avail)
    addr_num = socket.inet_pton(socket.AF_INET, client_addr)
    print " sending %s" % ' '.join("{:02x}".format(ord(c)) for c in addr_num)
    encrypted_num = encryption.encrypt(addr_num)
    n = sock.send(encrypted_num)
    print " sent %d bytes" % n
    return client_addr, avail+1

def process_packet(data, sock2addr, addr2sock, client_socket):
    if len(data) < 4:
        print "packet too short for IP, ignoring"
    decrypted = encryption.decrypt(data)
    # print_hex(decrypted)
    packet = scapy.all.IP(decrypted)
    dst_addr = packet[scapy.all.IP].dst
    if dst_addr == MY_ADDR:
        print " packet intended for server, handling"
        handle_ping(decrypted, client_socket)
    else:
	if dst_addr in addr2sock:
		sock = addr2sock[dst_addr]
            	print " packet intended for %s, routing" % dst_addr
            	route_packet(data, sock, dst_addr)
    	else:
       		print "addr %s not in network, ignoring" % dst_addr

def handle_ping(data, sock):
    packet = scapy.all.IP(data)
    if packet.haslayer(scapy.all.ICMP) and packet[scapy.all.ICMP].type == 8:
        print "  packet is ICMP echo-request, replying"
        pong = packet.copy()
        swap_src_and_dst(pong, scapy.all.IP)
        pong[scapy.all.ICMP].type='echo-reply'
        pong[scapy.all.ICMP].chksum = None   # force recalculation
        pong[scapy.all.IP].chksum   = None
        encrypted = encryption.encrypt(pong.build())
        sock.send(encrypted)
    else:
        print "  packet data not recognized, printing"
        print_hex(data)        

def route_packet(data, sock, dst_addr):
    print "  packet routed to %s on socket %d" % (dst_addr, sock.fileno())
    encrypted = encryption.encrypt(data)
    n = sock.send(encrypted)
    print "  sent %d bytes" % n

def swap_src_and_dst(packet, layer):
    packet[layer].src, packet[layer].dst = packet[layer].dst, packet[layer].src

def print_hex(data):
    data_hex = ' '.join("{:02x}".format(ord(c)) for c in data)
    print data_hex


if __name__ == "__main__":
    main()
