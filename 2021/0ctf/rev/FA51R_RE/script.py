import glob

def maximum():
	segments = [get_segm_end(s) for s in Segments()]
	return max(segments) + 0x1000 & ~0xfff

def load(path, base=None):
	code = open(path, 'rb').read()
	name = ('_' + path[:8]) if len(path) == 32 else path

	if base is None:
		base = maximum() + 0x1000

	if not ida_segment.get_segm_by_name(name):
		idaapi.add_segm(0, base, base + len(code) + 0x100, name, 'CODE')
		idaapi.patch_bytes(base, code)
		idaapi.set_name(base, 'do_' + name)

	segment = ida_segment.get_segm_by_name(name)
	base = segment.start_ea
	idaapi.set_segm_addressing(segment, 2)
	idaapi.create_insn(base)
	idaapi.add_func(base)

BSS_START = 0x700000000
def add(start, size, name):
	idaapi.add_segm(0, start, start + size, name, 'DATA')
	segment = ida_segment.get_segm_by_name(name)
	idaapi.set_segm_addressing(segment, 2)

add(BSS_START, 0x10000, 'bss')
add(0x300000, 0x1000, 'shared')

idaapi.patch_qword(0x300000, idaapi.get_name_ea(-1, 'dyn_call'))

load('rodata', 0x600000000)
for path in glob.glob('?' * 32):
	load(path)

def patch(name):
	ea = idc.find_text(here(), SEARCH_DOWN, 0, 0, ' call ')
	segments = [(addr, idc.get_segm_name(addr)) for addr in Segments()]
	segments = [entry for entry in segments if entry[1].startswith('_' + name)]
	assert len(segments) == 1
	target = segments[0][0]
	if idaapi.get_bytes(ea - 5, 5) == b'\xb8\x00\x00\x00\x00':
		idaapi.patch_bytes(ea - 5, b'\xe8' + struct.pack("<L", target - ea & 0xffffffff) + b'\x90\x90')
	elif idaapi.get_bytes(ea, 2) == b'\xFF\xD2':
		ea = idc.find_text(ea, SEARCH_UP, 0, 0, 'eax, offset ')
		idaapi.patch_bytes(ea, b'\x48\xba' + struct.pack("<Q", target) + b'\x90')
	elif idaapi.get_bytes(ea, 2) == b'\xFF\xD1':
		ea = idc.find_text(ea, SEARCH_UP, 0, 0, 'eax, offset ')
		idaapi.patch_bytes(ea, b'\x48\xb9' + struct.pack("<Q", target) + b'\x90')
	elif idaapi.get_bytes(ea, 2) == b'\xFF\xD0':
		ea = idc.find_text(ea, SEARCH_UP, 0, 0, 'xmm15, xmm0')
		idaapi.patch_bytes(ea, b'\x48\xb8' + struct.pack("<Q", target) + b'\x90\x90\x90')
	else:
		print(hex(ea))
