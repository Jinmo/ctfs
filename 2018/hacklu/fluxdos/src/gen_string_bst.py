import sys
sys.stdout = open(sys.argv[1], 'wb')
path = sys.argv[2]
print '(func $a'
for i, c in enumerate(bytearray(path + '\x00')):
	print '  (push u8 %d)' % c
	print '  (store u8 %d)' % (1000 + i)
print ')'
print '(export $a)'