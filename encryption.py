# VPN Encryption functions

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017

from itertools import cycle, izip

KEY = '3u5hjgniwm30,xw13--'

# Encryption
def encrypt(message):
    cyphered = ''.join(chr(ord(c)^ord(k)) for c,k in izip(message, cycle(KEY)))
    # print('%s ^ %s = %s' % (message, KEY, cyphered))

# Decryption
def decrypt(cyphered):
    message = ''.join(chr(ord(c)^ord(k)) for c,k in izip(cyphered, cycle(KEY)))
    # print('%s ^ %s = %s' % (cyphered, KEY, message))


