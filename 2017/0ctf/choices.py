# IDAPython

# BP on below (the function's usage is not too many, so you can use xrefs on it):
# 00007FFFF6701C3D call    __ZN4Oops11CryptoUtils10scramble32EjPKc ; Oops::CryptoUtils::scramble32(uint,char const*)
# Appcall-ed address is this function.

for i in range(100):
	print (Eval('Appcall(0x00007FFFF670B934, ParseType("int __usercall a<rax>(void *<rdi>, void *<rsi>, void *<rdx>)", 0), rdi, %d, rdx)' % i) & 0xffffffff)

# then give this to binary.