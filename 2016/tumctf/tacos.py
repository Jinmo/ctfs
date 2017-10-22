import socket
import sys
import random

primes = [3, 5, 7, 11, 13, 17, 19, 23, 29,
31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013,
1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151,
1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223]

def rw(t):
	d = ''
	while t not in d:
		c = s.recv(1)
		if c == '':
			print 'Socket Error'
			exit()

		if 31 < ord(c) < 128:
			sys.stdout.write(c)
		else:
			sys.stdout.write('.')

		d += c
	return d

def is_prime(n):
    for _ in range(5):
        if pow(random.randrange(1, n), n - 1, n) != 1:
            return False
    return True
# define of the local right shift function (>>>)
def rshift(val, n): return (val % 0x100000000) >> n
# define some magic XOR functions to be able to extract the state's number from the outputs server
def unBitshiftLeftXor(value, shift, mask):
        i = 0
        result = 0
        while (i * shift < 32):
                partMask = (rshift(-1, (32 - shift))) << (shift * i)
                part = value & partMask
                value ^= (part << shift) & mask
                result |= part
                i+=1
        return result
 
def unBitshiftRightXor(value, shift):
        i = 0;
        result = 0;
        while (i * shift < 32):
                partMask = rshift((-1 << (32 - shift)) , (shift * i))
                part = value & partMask
                value ^= rshift(part, shift)
                result |= part
                i+=1
        return result
# this function give us long number of the MT internal state
def back_state(out):
        value = unBitshiftRightXor(out, 18)
        value = unBitshiftLeftXor(value, 15, 4022730752)
        value = unBitshiftLeftXor(value, 7, 2636928640)
        return unBitshiftRightXor(value, 11)

isprime = is_prime
ran = random.Random()

p = 2 ** (2490-38*2)
p = 0x7b87850000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001L
q = 0x154c252dd38c81480000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002c22eceaa8001L
while True and 0:
	r = p * 2 ** random.randrange(1, 20)
	for c in random.sample(primes, random.randrange(1, 20)):
		r *= c
	r += 1
	if isprime(r) and r.bit_length() >= 2496:
		q = r
		break

assert 2 ** 1024 < p < q < 2 ** 4096
# assert is_prime(q)
assert not (q - 1) % p
# assert is_prime(p)

if True:
	ran.seed(1)
	state = list(ran.getstate()[1])
	g = ran.randrange(2 ** 32)
	print map(hex, state)
	s = g
	gs = []
	for i in range(1):
		gs.append(back_state(s & 0xffffffff))
		s >>= 32
	print map(hex, gs)
else:
	s = socket.create_connection(('104.198.63.175', 1729))
	s.send(str(q) + '\n')
	s.send(str(p) + '\n')
	g = int(rw(' '), 0)
	y = int(rw('\n'), 0)

