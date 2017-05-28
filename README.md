# CS60 Final Project: VPN Gateway and Client

##### James Edwards, Rick Dionne, Willy Wolfe

### Overview

We have implemented a VPN server and clients in Python. The server will run on a specified port on `flume.cs.dartmouth.edu`. Clients may then connect to the server via a tunnel interface and join a network with other clients to that server.

The code is split into 4 main files:

* `vpnserv.py` starts up the VPN server on `flume.cs.dartmouth.edu` port 8080. It will then accept connections and forward packets from clients using the given VPN client code.

* `vpncli.py` starts up the VPN client on the user's host machine. See instructions below for ensuring the host machine is properly configured.

* `pytun.py` contains a function for opening the tunnel interface within our client.

* `fakenet.py` contains functions for configuring the tunnel interface.

### Setup and Running

The code is all written in Python, so compilation is unnecessary. To run the server, simply run `vpnserv.py` from the command line. To start a client, first ensure that the tunnel interface is correctly configured. This is achieved with the command: `openvpn --mktun --dev tun0`. Then you may run `vpncli.py`, and any connections in the `10.10.0.0/24` range will be captured by the client program and forwarded to the VPN server.

### Testing

Testing involves starting the server on `flume.cs.dartmouth.edu`, and running the client program on at least two separate hosts. The test strategy we implemented is as follows:

1. Start VPN server by running `vpnserv.py` on `flume.cs.dartmouth.edu`.

2. Start VPN Client on first host.

3. Run test script on second host.

### Assumptions and Limitations

1. We did not implement security or encryption of any kind.

2. The client hosts must have root privilege.

3. The client hosts must have scapy installed.
