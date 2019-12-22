from string import uppercase
from itertools import product
from hashlib import md5
import struct

Src=[0]*8
Src[0] = 1816876302;
Src[1] = 1745554764;
Src[2] = 123095635;
Src[3] = 1392726285;
Src[4] = 1397424973;
Src[5] = 1733317741;
Src[6] = 151409428;
Src[7] = 1191647847;

data="""714d32d45f6cb3bc336a765119cb3c4c
51a96b38445ff534e3cf14c23e9c977f
51a96b38445ff534e3cf14c23e9c977f
bc9189406be84ec297464a514221406d
4ec6aa45006dae153d94abd86b764e17
51a96b38445ff534e3cf14c23e9c977f""".split('\n')

maps={x:None for x in data}

found=0
for x, y, z in product(uppercase, uppercase, uppercase):
	value=''.join((x, y, z))
	hash=md5(value).hexdigest()
	if hash in maps:
		maps[hash]=value
		found += 1
		if len(maps) == found:
			break

h=md5(''.join([maps[x] for x in data])).hexdigest()
data = zip(struct.pack("<8L", *Src), h)
data=bytearray([ord(x)^ord(y) for x, y in data])
print 'justCTF{%s}'%data