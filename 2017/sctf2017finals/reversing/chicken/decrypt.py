
v43 = [0] * 16
v43[0] = 96;
v43[1] = 117;
v43[2] = 102;
v43[3] = 119;
v43[4] = 106;
v43[5] = 0x6B;
v43[6] = 98;
v43[7] = 0x6B;
v43[8] = 96;
v43[9] = 122;
v43[10] = 99;
v43[11] = 105;
v43[12] = 127;
v43[13] = 101;
v43[14] = 106;
v43[15] = 105;
for i in range(len(v43)):
        v43[i] ^= i + 1

print bytearray(v43)
v26 = v43
v26[0] = 105;
v26[1] = 99;
v26[2] = 109;
v26[3] = 96;
v26[4] = 118;
v26[5] = 105;
v26[6] = 106;
v26[7] = 109;
v26[8] = 96;
v26[9] = 100;
v26[10] = 98;
v26[11] = 120;
v26[12] = 123;
v26[13] = 107;
v26[14] = 108;
v26[15] = 100;
for i in range(len(v43)):
        v43[i] ^= i + 1

print bytearray(v43[:16])


r = open('input/eggyolk', 'rb').read()
from Crypto.Cipher import AES

aes = AES.new('awesomecipherkey', AES.MODE_CBC, IV='handsomeinitvect')
open('output/1.dex', 'wb').write(aes.decrypt(r))

# Then analyzed 1.dex.

data = open('input/flag.enc', 'rb').read()
aes = AES.new(("kingodemperorchungmugongalmighty"), AES.MODE_CBC, IV=("superduperinjung"))
open('output/1.pdf', 'wb').write(aes.decrypt(data))
