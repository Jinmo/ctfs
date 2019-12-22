mem=bytearray(open('vm2.bin','rb').read())
print bytearray([mem[0x2000+i]^mem[0x14e+i]^mem[0x1e7+i]^i for i in range(0x2f)])