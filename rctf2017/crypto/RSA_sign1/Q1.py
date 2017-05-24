import socket
import rsa

s = socket.create_connection(('rsasign1.2017.teamrois.cn', 3000))

def rVerify(message, signature, pub_key): 
    n, e = pub_key
    blocksize = rsa.common.byte_size(n)
    encrypted = rsa.transform.bytes2int(signature)
    decrypted = rsa.core.decrypt_int(encrypted, e, n)
    clearsig = rsa.transform.int2bytes(decrypted, blocksize)
    try:
        sep_idx = clearsig.index(('\x00'), 2)
    except ValueError:
        print ('How ugly your signature looks...More practice,OK?')
        return False 
        
    signature = clearsig[sep_idx+1:]
    
    # Compare the real hash to the hash in the signature
    if message != signature:
        print `message`
        print `signature`
        print ('wanna cheat me,ah?')
        return False
    return True

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

n = 99103278939331174405096046174826505890630650433457474512679503637107184969587849584143967014347754889469667043136895601008192434248630928076345525071962146097925698057299368797800220354529704116063015906135093873544219941584758892847007593809714204471472620455658479996846811490190888414921319427626842981521
e = 3
pub_key = n, e
blocksize = rsa.common.byte_size(n)

orig = rsa.transform.bytes2int('jinmo123\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
root = find_cube_root(orig)
orig = root ** 3
signature = root
clearsig = rsa.transform.int2bytes(orig, blocksize)
signature = rsa.transform.int2bytes(signature, blocksize)
sep_idx = clearsig.index(('\x00'), 2)
message = clearsig[sep_idx+1:]
print `message`
print `signature.encode('hex')`
assert rVerify(message, signature, pub_key)
s.send(message + '\n')
s.send(signature.encode('hex'))
while True:
    d = s.recv(1024)
    if d == '':
        break
    print d