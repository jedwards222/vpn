#!/usr/bin/python

# VPN Server Implementation

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

import sys          # stdin
import socket       # socket
import select       # select
import scapy.all    # packet handling
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

# for client handling
read_list = [] # list of open sockets
sock2addr = {} # dict, fileno:addr_string
addr2sock = {} # dict, addr_string:socket

def main():
    """Set up the server, maintain client connections"""
    server_socket = init_tcp_socket() # init socket, set to listen
    read_list.append(server_socket)
    read_list.append(sys.stdin) # to listen for EOF
    sock2addr[server_socket.fileno()] = MY_ADDR
    addr2sock[MY_ADDR] = server_socket 
    avail = 2
    while True: # loop until EOF on stdin
        # wait for incoming packet on any connection
        readable, writable, errored = select.select(read_list, [], [])
        for sock in readable:
            if sock == sys.stdin:
                line = sys.stdin.readline()
                if line == '': # EOF
                    print "EOF received, shutting down server"
                    server_shutdown()
                    return 0 # exit
                else:
                    print "Host: %s" % line.rstrip()            
            elif sock == server_socket: # new connection
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
    """Initialize the tcp socket for clients to connect to

    keyword arguments:
     port: the port to listen on, defaults to global constant PORT
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # create socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # skip timeout
    sock.bind((HOST, port))                                    # bind to port
    sock.listen(BKLG)                                          # set to listen
    print "server_socket listening on port %d" % port
    return sock

def client_setup(avail, sock):
    """Set up a client connection, assign vpn ip
    
    arguments:
     avail: the lowest unused address suffix
     sock: the TCP socket of the new client
     addr: the vpn ip to assign
    """
    client_addr = NET_PREFIX + str(avail)                    # construct addr
    addr_num = socket.inet_pton(socket.AF_INET, client_addr) # convert to num
    encrypted_num = encryption.encrypt(addr_num)             # encrypt
    sock.send(encrypted_num)                                 # send
    return client_addr, avail+1

def process_packet(data, sock2addr, addr2sock, client_socket):
    """Process an incoming packet

    determine the intended recipient, then
    - if recipient, sender both in network, route packet
    - if recipient in network, sender not, forward incoming packet
    - if sender in network, recipient not, forward outgoing packet
    - if sender in network, recipient server, respond to ping

    arguments:
     data:          the (possibly encrypted) contents of the packet
     client_socket: the socket on which the packet was received
    """
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
    """Respond to ICMP echo-request from client
    
    identify an ICMP echo-request, and send the appropriate reply
    arguments:
     data: decrypted data of the packet
     sock: socket to reply on
    """
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
    """Route packet between clients in VPN
    
    route packet within private network
    arguments
     data:     encrypted packet
     sock:     socket to send to
     dst_addr: VPN address of destination
    """
    sock.send(data)
    print "  packet routed to %s on socket %d" % (dst_addr, sock.fileno())

def swap_src_and_dst(packet, layer):
    """Swap src and dst fields in packet at desired layer

    edit the fields in a scapy packet
     packet: packet to edit
     layer: layer to edit (eg IP, TCP)
    """
    packet[layer].src, packet[layer].dst = packet[layer].dst, packet[layer].src

def print_hex(data):
    """Print raw hex of packet; for debugging"""
    data_hex = ' '.join("{:02x}".format(ord(c)) for c in data)
    print data_hex

if __name__ == "__main__":
    main()
