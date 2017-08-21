# coding: utf8

# 스크립트에 나와있지 않은 모든 부분이 게싱 및 브포였습니다. 가령 커맨드는 2^16번 브포하였습니다. CRC는 앞에 넣어보고 뒤에 넣어봤는데 뒤가 맞았습니다.
# 플래그: SCTF{WoW!NowYouCanHackUnknownProtocol!}

import socket
import struct
import os
import json
import random
import zlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('hackthedrone.eatpwnnosleep.com', 31234))

YOUR_API_KEY = u"43073909ecc48af12aa63c8f74989bc9523587eca49d37c97edd3027984e6101"

a = {
    'apikey' : YOUR_API_KEY,
}

s.send(json.dumps(a).encode())
print (s.recv(102400))

uid = 9999
def encode(x, cmd=0):
	L = struct.pack("<LHH", len(x) + 12, uid, cmd)
	crc = zlib.crc32(L + x) & 0xffffffff
	return L + x + struct.pack("<L", crc)


def mutate(x):
	x=bytearray(x)
	count = random.randrange(20)
	for i in xrange(count):
		i = random.randrange(0, len(x) * 8)
		x[i/8] |= 1 << (i%8)
	return str(x)

print s.recv(102400)
a = '\x00' * 0
pack = encode(a)
s.send((pack).encode('hex') + '\n')
x = s.recv(102400).strip()
x = x.decode('hex')
if x not in ('[-] Packet length does not match with the header', '[-] Too short packet'):
	print x
	if 'uid is' in x:
		uid = int(x.split(' ')[-1])
	print `pack`
def recvline():
	d = ''
	while '\n' not in d:
		c = s.recv(1)
		if c == '':
			break
		d += c
	return d.strip()

def cmd(i, recvcnt, a='\x00' * 0):
	pack = encode(a, i)
	s.send((pack).encode('hex') + '\n')
	x = recvline()
	x = x.decode('hex')
	if x not in ('[-] Packet length does not match with the header', '[-] Too short packet') and 'Unknown command' not in x or 1:
		print x
		if 'uid is' in x:
			uid = int(x.split(' ')[-1])
		print `pack`
	for i in range(recvcnt):
		x = recvline()
		x = x.decode('hex')
		print '%02d' % i, x

i = 0x1212
if 1:
	# ['help', 'print_location', 'control_rotor', 'change_altitude', 'moveto', 'change_mode']
	# cmd(0x1212, 3) # help: description
	cmd(0x3030, 5) # print_location: map
	# cmd(0x4040, 3) # control_rotor: rotor control (calibrating)
	# cmd(0x6666, 1) # change_altitude: change altitude (armed)
	# cmd(0x7878, 1) # moveto: set the waypoint of drone (armed)
	# cmd(0xfefe, 2, 'z') # change mode: DISARMED (0) / ARMED (1) / CALIBRATING (2)
	# cmd(0x7878, 1)
	cmd(0xfefe, 2, struct.pack("<H", 2))
	for i in range(17, 21):
		cmd(0x4040, 2, chr(i)+struct.pack("<H", 0)) # control_rotor: rotor control (calibrating)
		cmd(0x4040, 3, chr(i)+struct.pack("<H", 0xffff)) # control_rotor: rotor control (calibrating)
	cmd(0xfefe, 2, struct.pack("<H", 1))
	cmd(0x6666, 3, struct.pack("<f", 1000)) # change_altitude: change altitude (armed)
	import time
	time.sleep(6)
	cmd(0x7878, 3, struct.pack("<ff", 60, 48)) # moveto: set the waypoint of drone (armed)
	time.sleep(11)

	cmd(0x7878, 2, struct.pack("<ff", 53, 16)) # moveto: set the waypoint of drone (armed)
	time.sleep(11)

	cmd(0x7878, 4, struct.pack("<ff", 25, 16)) # moveto: set the waypoint of drone (armed)
	cmd(0x6666, 100, struct.pack("<f", 0))
	time.sleep(16)
exit()
prev = 0xfeff
prevcmd = -1
for i in range(prev, 65536):
	s.send(encode('', i).encode('hex') + '\n')
	if i % 3 == 0:
		x = recvline().decode('hex')
		if 'Unknown command' not in x:
			print hex(prevcmd+1), x
			exit()
		else:
			prevcmd = int(x.split(': ')[1])
		if x == '':
			print 'connection..'
			break
		prev = i

while False:
	x = recvline().decode('hex')
	if 'Unknown command' not in x:
		print hex(prevcmd + 1), x
	else:
		prevcmd = int(x.split(': ')[1])