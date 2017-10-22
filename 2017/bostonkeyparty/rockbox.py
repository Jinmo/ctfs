s = "GLI|nuXdfkXfmt)Ximf~Xjrtndz"
s = bytearray(s)
x = 6
y = 1
s = bytearray([(x ^ a) + y for a in s])
print s