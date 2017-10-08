from z3 import *
from multiprocessing import Pool
import socket
import telnetlib

# Thanks to crit3ri4.
a = 2569194187569403613
b = 9846075293684566698
c = 10463413796919233944
d = -345490962550008701

x = BitVec('x', 64)

def run(data):
	solver = Solver()
	solver.add(data == x * (c + x * (a * x - b)) - d)
	if solver.check() == unsat:
		return ''
	return '%016X' % solver.model()[x].as_long()

if __name__ == '__main__':
	p = Pool(4)
	while True:
		try:
			s = socket.create_connection(('195.133.196.43', 27777))
			t = telnetlib.Telnet()
			t.sock = s

			data = s.recv(1024)
			data = data.split(': ')[1]
			result = ''
			data = [int(data[i:i+16], 16) for i in range(0, 64, 16)]
			result = ''.join(p.map(run, data))
			print len(result)
			if len(result) != 64:
				assert False

			s.send(result + '\n')
			print s.recv(1024)
			t.interact()
		except AssertionError:
			s.close()
			continue