# CS60 Final Project: VPN Gateway and Client

##### James Edwards, Rick Dionne, Willy Wolfe

### Overview

We have implemented a VPN server and clients in Python. The server will run on `wolfe.cloudapp.net` port 5000. Clients may then connect to the server via a tunnel interface and join a network with other clients to that server.

We also some additional functions for our VPN for extra credit. They are listed at the end of the README.

The code is split into 4 main files:

* `vpnserv.py` starts up the VPN server on `wolfe.cloudapp.net` port 5000. It will then accept connections and forward packets from clients using the given VPN client code.

* `vpncli.py` starts up the VPN client on the user's host machine. See instructions below for ensuring the host machine is properly configured.

* `pytun.py` contains a function for opening the tunnel interface within our client.

* `fakenet.py` contains functions for configuring the tunnel interface.

### Grading

Please grade the master branch, tag: June1. Let us know if there are any issues with the server running and we can provide the credentials for signing in to Willy's Azure account.

### Setup and Running

The code is all written in Python2.7, so compilation is unnecessary.
To run the server, simply run `vpnserv.py` from the command line. The server code will already be running on our host, Willy's Microsoft Azure server: `will@wolfe.cloudapp.net`
To start a client, first ensure that the tunnel interface is correctly configured. 
This is achieved with the command: `openvpn --mktun --dev tun0`. Additionally, the `setup.sh` script can be run to perform this command.
Then you may run `vpncli.py`, and any connections in the `10.10.0.0/24` range will be captured by the client program and forwarded to the VPN server.

### Testing

Testing involves starting the server on `wolfe.cloudapp.net:5000`, and running the client program on at least two separate hosts. The test strategy we implemented is as follows:

1. Start VPN server by running `vpnserv.py` on `wolfe.cloudapp.net`.
2. Start VPN Client on two hosts: they receive the addresses 10.10.0.2 and 10.10.0.3
3. Host 2 pings Host 3 - successful
4. Host 3 pings Host 2 - successful
5. Both hosts ping the server - successful
6. Both hosts ssh into each other - successful
7. Host disconnects and reconnects - is given new network IP address - successful
8. Runnning testserver.sh on one client and testclient.sh on another client to ensure UDP/TCP connectivity 
9. To run testing scripts use ``testserver.sh <client ip> <port>`` and ``testclient.sh <server ip> <port>``


### Assumptions and Limitations

1. The client hosts and server host must have root privilege.
2. Running on linux client only.
3. Running with Python 2.7
4. The client hosts and server host must have scapy installed.
5. No connection to outside internet yet (still working on NAT).
6. The clients are not remembered when disconnecting and reconnecting.

## Extra Credit

Two additional features were added on top of the required base functionality for the VPN:

1. Encryption - a simple encryption using a shared secret key is used to hide all traffic between clients and the server. This includes connections between clients that go through the server. The code used by encryption lives in `encryption.py`

2. NAT (UNFINISHED) - we started to implement most of the features of project option 1 and allowed our VPN clients to connect to the outside internet through our VPN. This feature is still in a separate branch, and will be worked on more for Sergey to grade by the June 5th deadline. See notes on our [NAT configuration](https://gitlab.cs.dartmouth.edu/jgedwards/cs60project/blob/nat/CONFIGURATION.md)
