from pwn import *
from glob import glob
from unicorn.x86_const import *
import os
from base64 import *
from unicorn import *

uc = Uc(UC_ARCH_X86, UC_MODE_64)
uc.mem_map(0, 4096 * 4096)
STACK = 0x10000000
uc.mem_map(STACK, 0x100000)
STACK_START = STACK + 0x100000

def addr(x):
	return int(x.strip().split(':')[0],16)

def process(data, buf):
	lines = buf.strip().split('\n')
	for line in lines:
		if 'callq' in line:
			exit_handler = int(line.split('\t')[-1].split('<')[0].strip().split(' ')[-1], 16)
			break
	start = addr(lines[0])
	end = addr(lines[-1])
	print hex(start)
	print hex(end)
	uc.mem_write(exit_handler, '\xcc')
	uc.mem_write(start, data[start:end + 1])
	for i in range(32, 256):
		uc.reg_write(UC_X86_REG_RSP, STACK_START)
		uc.reg_write(UC_X86_REG_RDI, i)
		try:
			uc.emu_start(start, end)
			return start, i
		except UcError as e:
			continue
	print 'what?'
	exit()

r = remote('smokeme.420blaze.in', 42069)
r.recvline()

def gen(in_, out_):
	os.system('objdump -d %s > %s' % (in_, out_))

def go(path):
	name = path.split('/')[-1]
	print name
	disas = '/tmp/%s' % name
	if os.path.isfile(disas + '.out'):
		return r.sendline(open(disas + '.out').read())
	if not os.path.isfile(disas):
		gen(path, disas)
	data = open(path, 'rb').read()
	baseAddr = data.find('\xbf\xfa\x00\x00\x00')
	bStr = '   %x' % baseAddr
	disass = open(disas, 'rb')
	start, start2 = False, False
	buf = ''
	bufs = []
	flag = ''
	for line in disass:
		if start:
			if 'ret' in line:
				if bufs:
					startAddress, c = process(data, buf)
					flag += chr(c)
					if startAddress == lastCall:
						break
				bufs.append(buf)
				buf = ''
			else:
				if ',%rsp' in line and 'sub' in line: buf = ''
				buf += line
		elif line.startswith(bStr):
			start = True
		elif 'callq' in line and '%' not in line:
			lastCall = int(line.split('\t')[-1].split('<')[0].strip().split(' ')[-1], 16)

	open(disas + '.out', 'wb').write(b64encode(flag))
	r.sendline(b64encode(flag))

while True:
	data = r.recvline().strip()
	print data
	path = 'smokeme420_dist/' + data
	go(path)
r.interactive()
