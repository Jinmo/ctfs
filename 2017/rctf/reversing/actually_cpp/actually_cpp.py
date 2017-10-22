from Crypto.Cipher import AES
import struct
key = '''      si32(-536244034,ebp - 12);
      si32(2108577555,ebp - 16);
      si32(-1182021347,ebp - 20);
      si32(-1993905352,ebp - 24);
      si32(252579084,ebp - 28);
      si32(185207048,ebp - 32);
      si32(117835012,ebp - 36);
      si32(50462976,ebp - 40);'''.split('\n')
key = [x.split('(')[1].split(',')[0] for x in key]
key = [eval(x) for x in key][::-1]
key = [struct.pack("<L", x & 0xffffffff) for x in key]
key = ''.join(key)
key = bytearray(key)
# bf part
key[21] += 5
key[17] -= 5
key[20] += 2
key[11] -= 5
iv, key = key[:16], key[16:]
iv, key = str(iv), str(key)

from glob import glob

s = '\xd5\x18a\x03\x1e\x1c\x95:b\xc2\x93\x8b9b5\xb1\xf3d\x94/3\x95B#\xd3l&\x88\xab*?G\x94(\xb4F\xa5\t\x04!\xac\x1f\x82\xba\xb4\xb3(N\xc0\xbc\xefS\xfcC1\\\xda|\x83\xd0\xfa\x90\xb5\x9f'
aes = AES.new(key, AES.MODE_CBC, IV=iv)
d = aes.decrypt(s)
print `d`
if 1 <= ord(d[-1]) <= 0x10 and d.endswith(ord(d[-1]) * d[-1]):
	print `d`