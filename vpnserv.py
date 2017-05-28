#!/usr/bin/python

# VPN Server Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

# PSEUDOCODE
# 
# 1. setup_socket(port = 8080)
# 2. while (true)
# 3.    data = read_socket()
# 4.    if (data.len > 0)
# 5.    resp = parse_socket()
# 6.    send_resp(resp)
#


import socket
import select

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
                client_socket, address = server_socket.accept()     # accept connnection
                read_list.append(client_socket)                     # add to list
                # set up a VM address associated with this client connection
                client_dict[sock.fileno()], avail = client_setup(address, avail) 
            else:
                data = sock.recv(IP_MAXPACKET) # get packet from client 
                if data:
                    process_packet(data, client_list) # handle packet
                else: 
                    del client_dict[sock.fileno()] # remove from client dict
                    sock.close()                   # close this connection
                    read_list.remove(sock)         # remove from read_list

def init_tcp_socket(port=PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # create the socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # skip timeout
    sock.bind((HOST, port))                                      # bind to a port
    sock.listen(BKLG)                                          # set port to listen
    print "server_socket listening on port %d" % port
    return sock

def client_setup(address, avail):
    return NET_PREFIX + str(avail), avail+1

def process_packet(data, client_list):
    return

if __name__ == "__main__":
    main()
