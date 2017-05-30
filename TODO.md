# TODO for Encryption

### Option 1: Encrypt stream (simple option)

1. Choose encryption algorithm to use.

2. Encrypt each data packet sent in `vpncli`.

3. Decrypt each data packet received in `vpncli` or in `vpnserv`

---

##### Specifics:

Client and Server decide on a key (maybe start with it hardcoded in to both).
The data is XOR'ed with this key (maybe the key is repeated to ensure that it covers the whole data, or just make the key very long
This XOR occurs both on sending and receiving a packet.

### Option 2: New protocol with encryption (harder)

1. Read more about OpenVPN's encryption protocol.
