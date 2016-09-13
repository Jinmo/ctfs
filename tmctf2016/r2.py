import os
import time
from hashlib import md5
from Crypto.Cipher import AES
n = 19600411981265698127825276498725775640189153141051083923744581877282066374129140308065084126378450572154710507455046229264042891865368049588254043024699723830681736944487782474589430621555428025094874648325087533221454681869241762811041485584302179072036660061861881297659000145330394098105589714963217814420685181300603480626953568574509336737923587275465337451036716039313654514434256137226575843918542227084381418040868556729347066661412015560155343194886850611275246841186443931400742699485448338707536191495990749490625001209307284386288614998905162164889085393112399477468760335941882032761110618227183053642177
e = 65537
path = '../../../Downloads/DecryptMe/FLAG.docx.tmd'
t = os.path.getmtime(path)
t = int(t)

f = open(path, 'rb')
f.seek(-264, 2)
nonce = f.read(256)
nonceRSA = int(nonce.encode('hex'), 16)
f.seek(0, 0)

def rand():
	global r
	v0 = (0x15A4E35 * r + 1) & 0xffffffff;
	r = v0 & 0xffffffff;
	return (r >> 16) & 0x7FFF;

def srand(seed):
	global r
	r = seed
	return rand()

seed = 1468585263

if seed is None:
	for pid in range(10000, 50000):
		seed = pid ^ t
		srand(seed)
		data = str(bytearray(rand() % 256 for i in range(16)))
		dataRSA = int(data.encode('hex'), 16)
		if pow(dataRSA, e, n) == nonceRSA:
			print 'yeah', seed
			break
		s = md5(data).digest()

srand(seed)
data = str(bytearray(rand() % 256 for i in range(16)))
print `data`
print pow(int(data.encode('hex'), 16), e, n) == nonceRSA