import rsa
import hashlib
import rsa
import binascii
import os
from gmpy2 import mpz, iroot, powmod, mul, t_mod
def to_bytes(n):
    """ Return a bytes representation of a int """
    return n.to_bytes((n.bit_length() // 8) + 1, byteorder='big')

def from_bytes(b):
    """ Makes a int from a bytestring """
    return int.from_bytes(b, byteorder='big')

def get_bit(n, b):
    """ Returns the b-th rightmost bit of n """
    return ((1 << b) & n) >> b

def set_bit(n, b, x):
    """ Returns n with the b-th rightmost bit set to x """
    if x == 0: return ~(1 << b) & n
    if x == 1: return (1 << b) | n

def cube_root(n):
    return int(iroot(mpz(n), 3)[0])
HASH_ASN1 = {
'MD5': ('\x30\x20\x30\x0c\x06\x08\x2a\x86\x48\x86\xf7\x0d\x02\x05\x05\x00\x04\x10'),
'SHA-1': ('\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14'),
'SHA-256': ('\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20'),
'SHA-384': ('\x30\x41\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x02\x05\x00\x04\x30'),
'SHA-512': ('\x30\x51\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x03\x05\x00\x04\x40'),
}

def rVerify(message, signature, pub_key): 
    blocksize = rsa.common.byte_size(pub_key[0])
    encrypted = rsa.transform.bytes2int(signature)
    decrypted = rsa.core.decrypt_int(encrypted, pub_key[1], pub_key[0])
    clearsig = rsa.transform.int2bytes(decrypted, blocksize)
    
    if clearsig[0:2] != ('\x00\x01'):
        print ('How ugly your signature looks...More practice,OK?')
        return False
    
    try:
        sep_idx = clearsig.index(('\x00'), 2)
    except ValueError:
        print ('RU Kidding me?')
        return False           
    
    (method_name, signature_hash) = rfind_method_hash(clearsig[sep_idx+1:])
    message_hash = rsa.pkcs1._hash(message, method_name)
    
      
    if message_hash != signature_hash:
          print ('wanna cheat me,ah?')
          return False
    return True

def rfind_method_hash(method_hash): 
    for (hashname, asn1code) in HASH_ASN1.items():
        if not method_hash.startswith(asn1code):
            continue
        return (hashname, method_hash[len(asn1code):])
    print ('How ugly your signature looks...More practice,OK?')
    exit(0)

def find_cube_root(n):
    lo = 0
    hi = n
    while lo < hi:
        mid = (lo+hi)//2
        if mid**3 < n:
            lo = mid+1
        else:
            hi = mid
    return lo

n = 99103278939331174405096046174826505890630650433457474512679503637107184969587849584143967014347754889469667043136895601008192434248630928076345525071962146097925698057299368797800220354529704116063015906135093873544219941584758892847007593809714204471472620455658479996846811490190888414921319427626842981521L
e = 3

count = 0
message = 'jinmo123%d' % count
signature = rsa.pkcs1._hash(message, 'MD5')
signature = '\x00' + '\x30\x20\x30\x0c\x06\x08\x2a\x86\x48\x86\xf7\x0d\x02\x05\x05\x00\x04\x10' + signature
pad = 1 << (len(signature) * 8 + 32)
suffix = signature
sig_suffix = 1
for b in range(len(suffix)*8):
    if get_bit(sig_suffix ** 3, b) != get_bit(rsa.transform.bytes2int(suffix), b):
        sig_suffix = set_bit(sig_suffix, b, 1)
while True:
    prefix = b'\x00\x01' + os.urandom(1024//8 - 2)
    sig_prefix = rsa.transform.int2bytes(cube_root(rsa.transform.bytes2int(prefix)))[:-len(suffix)] + b'\x00' * len(suffix)
    sig = sig_prefix[:-len(suffix)] + rsa.transform.int2bytes(sig_suffix)
    if b'\x00' not in rsa.transform.int2bytes(rsa.transform.bytes2int(sig) ** 3)[:-len(suffix)]: break

print `sig`

key = n, e
rVerify(message, sig, key)

import socket

s = socket.create_connection(('rsasign2.2017.teamrois.cn', 3001))
print s.recv(1024)
s.send(message + '\n')
print s.recv(1024)
s.send(sig.encode('hex') + '\n')
print s.recv(1024)