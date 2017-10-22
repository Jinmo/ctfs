import socket
import sys
from decimal import *

getcontext().prec = 100
HOST, PORT = 'misc.chal.csaw.io', 8000

s = socket.create_connection((HOST, PORT))
def rw(t):
	d = ''
	while t not in d:
		c = s.recv(1)
		if c == '':
			print 'Socket Error'
			exit()
		sys.stdout.write(c)
		d += c
	return d

while True:
	target = rw('\n').strip('$').strip('\n')
	target = Decimal(target)
	coins = '10000', '5000', '1000', '500', '100', '50', '20', '10', '5', '1', '0.5', '0.25', '0.1', '0.05', '0.01'
	coins = [Decimal(x) for x in coins]
	target_coins = [0] * len(coins)
	print target,
	for i, coin in enumerate(coins):
		while coin <= target:
			print target, coin
			target -= coin
			target_coins[i] += 1

	print target_coins

	for coin in target_coins:
		rw(':')
		s.send(str(coin) + '\n')

	rw('\n')