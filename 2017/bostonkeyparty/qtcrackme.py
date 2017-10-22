import numpy as np
from numpy.linalg import inv as inv_matrix # really???
from z3 import *

ciphertext = [342868586L, 276196100L, 719703660L, 771095780L, 607388058L, 526903709L, 1078504063L, 1277609804L, 380802638L, 328226818L, 869243743L, 752195599L, 503103844L, 346660259L, 739251810L, 732552923L]
key = [37087L, 28860L, 61271L, 23190L, 53230L, 21769L, 32974L, 3360L, 57679L, 1806L, 42054L, 12230L, 60656L, 21333L, 30763L, 25687L]
key2 = [4992L, 9722L, 3242L, 226L, 1252L, 22234L, 6753L, 4671L, 9993L, 259L, 3591L, 192L, 8245L, 5425L, 32L, 3527L]
key3 = [2282688058L, 383276719L, 93319952L, 3639096956L]
key3 = [key3[0] | (key3[1] << 32), key3[2] | (key3[3] << 32)]

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

concat = lambda x: sum([a << ((len(x) - b - 1) * 16) for a, b in zip(x, range(0, len(x)))])
mask = 2 ** 64 - 1
mask16 = 2 ** 16 - 1

def minor(matrix,i):
    """Returns the Minor M_0i of matrix"""
    minor = matrix
    del minor[0] #Delete first row
    for b in list(range(len(matrix))): #Delete column i
        del minor[b][i]
    return minor

def det(A):
    """Recursive function to find determinant"""
    if len(A) == 1: #Base case on which recursion ends
        return A[0][0]
    else:
        determinant = 0
        for x in list(range(len(A))): #Iterates along first row finding cofactors
            print("A:", A)
            determinant += A[0][x] * (-1)**(2+x) * det(minor(A,x)) #Adds successive elements times their cofactors
            print("determinant:", determinant)
        return determinant

def encrypt(input):
	global concat, key3
	s = [a ^ b for a, b in zip(input, key)]
	s = [concat(s[i:i+4]) for i in range(0, len(s), 4)]
	print map(hex, s)

	for i in range(2):
		key3_ = list(key3)
		a = s[i*2]
		b = s[i*2+1]
		for j in range(32):
			a = (key3_[1] ^ (ror(a, 8, 64) + b)) & mask
			b = (rol(b, 3, 64) ^ a) & mask
			# keystream
			key3_[0] = (j ^ (ror(key3_[0], 8, 64) + key3_[1])) & mask
			key3_[1] = (rol(key3_[1], 3, 64) ^ key3_[0]) & mask
			print hex(a), hex(b)
		s[i*2], s[i*2+1] = a, b

	# print map(hex, s)
	s2 = []
	for c in s:
		s2.append((c >> 48) & mask16)
		s2.append((c >> 32) & mask16)
		s2.append((c >> 16) & mask16)
		s2.append(c & mask16)

	# print map(hex, s2)

	s3 = [None] * 16
	for i in range(4):
		for j in range(4):
			s3[j*4+i] = key2[j*4+0] * s2[i] + key2[j*4+1] * s2[i+4] + key2[j*4+2] * s2[i+8] + key2[j*4+3] * s2[i+12]
			if s3[j*4+i] > 2**32:
				print 'wtf'
				exit()

	# print map(hex, s3)
	# print map(hex, ciphertext)
	return s3

def decrypt(input):
	global concat, key3, key2, mask
	s2 = [Int('s2[%d]' % i) for i in range(16)]
	s3 = [None] * 16
	for i in range(4):
		for j in range(4):
			s3[j*4+i] = key2[j*4+0] * s2[i] + key2[j*4+1] * s2[i+4] + key2[j*4+2] * s2[i+8] + key2[j*4+3] * s2[i+12]
	solver = Solver()
	for i in range(16):
		solver.add(s3[i] == input[i])
	if solver.check() == unsat:
		print 'wtf'
		exit()
	s2 = [solver.model()[s2[i]] for i in range(16)]
	s2 = map(lambda x: x.as_long(), s2)
	print map(hex, s2)
	s = [concat(s2[i:i+4]) for i in range(0, len(s2), 4)]
	for i in range(2):
		key3_ = list(key3)
		keys = []
		for j in range(32):
			# keystream
			keys.append([key3_[0], key3_[1]])
			key3_[0] = (j ^ (ror(key3_[0], 8, 64) + key3_[1])) & mask
			key3_[1] = (rol(key3_[1], 3, 64) ^ key3_[0]) & mask
		a = s[i*2]
		b = s[i*2+1]
		for j in range(32):
			print hex(a), hex(b)
			b = (ror(b ^ a, 3, 64)) & mask
			a = ((rol((keys[-1 - j][1] ^ a) - b, 8, 64))) & mask
		s[i*2], s[i*2+1] = a, b
	plaintext = []
	for c in s:
		plaintext.append((c >> 48) & mask16)
		plaintext.append((c >> 32) & mask16)
		plaintext.append((c >> 16) & mask16)
		plaintext.append(c & mask16)
	plaintext = [a ^ b for a, b in zip(plaintext, key)]
	print plaintext
	# print map(hex, s)
	mask = 2 ** 64 - 1

	# print map(hex, s3)
	# print map(hex, ciphertext)
	return str(bytearray(plaintext))

assert concat([1, 2, 3, 4, 5, 6, 7, 8]) == 0x10002000300040005000600070008

input = 'JINMO123JINMO123'
input = bytearray(input)
decrypt(encrypt(input))
print '=' * 500
print decrypt(ciphertext)