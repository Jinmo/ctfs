T = bytearray('CA\xcc\xd6\x8e\xe10\x87\xd8\xda\xe6\xc41\xb9T\xe3\x91-\x08r\xb3\xb3$\x0f`Dq0\x17\xd4y"0\xa2\x97\xa4\xaf8\'')

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
 
max_bits = 16  # For fun, try 2, 17 or other arbitrary (positive!) values
 
r = []
for i in range(len(T)):
	T[i]=(T[i]*2)&0xff
	r.append(ror(T[i], i % 8, 8))

print r
print `bytearray(r)`