import angr, claripy

p = angr.Project('/=/Downloads/angrybird')
cfg = p.analyses.CFG()

e = p.factory.entry_state(addr=0x4007da)
base = e.regs.rsp - 0x800
e.regs.rbp = base
input = claripy.BVS('input', 8 * 21)
e.memory.store(base - 0x50, input)
pg = p.factory.path_group(e)
def puts(a, b):
	print 'puts'
p.hook(0x400590, puts)
pg.explore(avoid=0x400590, find=0x404fab)
found = pg.found[0]
print `found`
print `found.state.se.any_str(input)`