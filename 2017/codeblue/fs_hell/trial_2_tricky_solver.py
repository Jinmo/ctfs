import string
import os
import multiprocessing

def run(text):
	path = 'tmp/x' + text[-1].encode('hex')
	open(path, 'wb').write(text)
	r = os.system('./fs_hell program_.txt %s|grep Congratz' % path)
	os.unlink(path)
	if r == 0:
		print 'found:', text
		return True
def main():
	p = multiprocessing.Pool(8)
	r = 'CBCTF{'
	for i in range(len(r), 100):
		cnt = i + 1
		open('program_.txt', 'wb').write(open('instrumented.txt' ,'r').read().replace('XXX', str(0x10000-cnt)))
		r += string.printable[p.map(run, [r + k for k in string.printable]).index(True)]

if __name__ == '__main__':
	main()