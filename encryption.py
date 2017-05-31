# VPN Encryption functions

# James Edwards, Rick Dionne, Willy Wolfe
# May 2017
# encrypt and decrypt from : https://dustri.org/b/elegant-xor-encryption-in-python.html

from itertools import cycle, izip
import random
import string

KEY = '{$O2*C~kLkpNrYGtas842au392vxm!N.gGjWc}MBg'

# Encryption
def encrypt(message):
    cyphered = ''.join(chr(ord(c)^ord(k)) for c,k in izip(message, cycle(KEY)))
    # print('%s ^ %s = %s' % (message, KEY, cyphered))
    return cyphered

# Decryption
def decrypt(cyphered):
    message = ''.join(chr(ord(c)^ord(k)) for c,k in izip(cyphered, cycle(KEY)))
    # print('%s ^ %s = %s' % (cyphered, KEY, message))
    return message

def generate_key(size):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.punctuation + string.digits) for _ in range(size))
