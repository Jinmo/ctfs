import ctypes, struct, subprocess

def func(buffer):
	global op0, op1, a, b, prec, width, pad
	prec, width = struct.unpack("<LL", buffer[:8])
	pad = struct.unpack("<L", buffer[16:20])[0]
	a, b = buffer[12], buffer[13]
	if a & 0x20:
		op0 = f'*(int *)&mem[{width:x}]'
	elif a & 0x40:
		op0 = f'*(int *)&mem[regs[{width}]]'
	else:
		op0 = f'regs[{width}]'
	if b & 2:
		op1 = f'*(int *)&mem[0x{prec:x}]'
	elif a & 2:
		op1 = f'*(int *)&mem[regs[{prec}]]'
	elif a & 1:
		op1 = f'{prec}'
	elif a & 4:
		op1 = f'regs[{prec}]'
	else:
		op1 = f'0'
	return 0

data = open('weather', 'rb').read()[0x4080:]
fmts = data[0xc8:]
data = bytearray(data)
data[0xc8:0xc8+len(fmts)] = [x^0x71^0x25 for x in fmts]
pc = 52

def do_M():
	return f'{op0} = {op1}'

def do_I():
	return f'{op0} &= {op1}'

def do_L():
	return f'{op0} <<= {op1}'

def do_U():
	return f'{op0} |= {op1}'

def do_O():
	return f'{op0} -= {op1}'

def do_E():
	return f'{op0} ^= {op1}'

def do_S():
	return f'{op0} += {op1}'

def do_N():
	return f'{op0} %= {op1}'

def do_X():
	return f'{op0} *= {op1}'

def do_V():
	return f'{op0} /= {op1}'

def do_C():
	if a & 0x20:
		op = f'if(regs[{prec}] < 0) '
	elif a & 0x40:
		op = f'if(regs[{prec}] > 0) '
	elif pad == 0x30:
		op = f'if(regs[{prec}] == 0) '
	else:
		op = ''
	return op + f'L{width}()'

queue = [pc]
visited = set()

import io

out = io.StringIO()

print("""
volatile char mem[0x2000];
volatile int regs[5];

""", file=out)

while queue:
	pc = queue.pop(0)
	if pc in visited:
		continue
	visited.add(pc)
	ops = data[pc:].split(b'\x00')[0]
	print(f'void L{pc}(){{//', ops, file=out)
	ops = ops.split(b'%')
	assert ops[0] == b'', pc
	for op in [x.decode() for x in ops[1:]]:
		fmt = op[-1]
		minus = op[0] == '-'
		ret = subprocess.run(['./printf-dump', '%' + op], stdout=subprocess.PIPE).stdout
		func(ret)
		text = eval('do_' + fmt)() + ';'
		if fmt == 'C':
			target = int(text.split('L')[-1].split('(')[0])
			queue.append(target)
		print('  ' + text, '//', op, file=out)
	print(f'}}', file=out)

print("""
int main() {
	L52();
}
""", file=out)
for x in visited:
	print(f"void L{x}();")
print(out.getvalue())