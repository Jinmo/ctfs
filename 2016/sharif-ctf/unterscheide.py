from fractions import gcd
from Crypto.Cipher import AES
import Crypto.Util.number

long_to_bytes = Crypto.Util.number.long_to_bytes
bytes_to_long = Crypto.Util.number.bytes_to_long

A = []
for line in open('../../../unterscheide/enc.txt', 'r'):
	A.append(int(line))

B = []
for i in range(len(A)-1):
	B.append(A[i+1] - A[i] - 1)

C = []
for i in range(len(B)-1):
	C.append(abs(B[i+1] - B[i]))

q = reduce(lambda x, y: gcd(x, y), C, C[0])
# print A[0] % q - 1 == A[1] % q - 2
rand = A[0] % q - 1
assert q * rand
print q, rand
# print A[0] % (q * rand) - 1
# print rand
# print len(bin(q))
# print pow(2, p1 * p2, q)
p1, p2 = 9090368507916642523150386537322321669636426087368916042946887058939035329547274618743911402935105936038626517888669029591219526735351668782037241444579211, 9090368507916642523150386537322321669636426087368916042946887058939035329547274618743911402935105936038626517888669029591219526735351668782037241434579031
p1, p2 = min(p1, p2), max(p1, p2)
a = A[0]
A = [(x - (rand + 1 + i)) / (q * (rand + i)) for i, x in enumerate(A)]
#A = [(x * (q * (rand + i))) + rand + i + 1 for i, x in enumerate(A)]
key = long_to_bytes(rand).rjust(128, '\x00')
a2 = A[0]
A = [int(pow(x, p1 * 2, q) == 1) for x in A]
print '\n'.join(map(hex, A))
print A
A = [str(x) for x in A]
A = ''.join(A)
A = '0' * (8 - len(A) % 8) + A
B = A
A = [chr(int(A[i:i+8], 2)) for i in range(0, len(A), 8)]
A = ''.join(A)
print len(A), len(B)
print bin(bytes_to_long(A))[2:]
print B
IV = key[16:32]
mode = AES.MODE_CBC
aes = AES.new(key[:16], mode, IV=IV)
print `aes.decrypt(A)`
print A