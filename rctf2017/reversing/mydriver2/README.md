# MyDriver2

It hook NtCreateFile with own routine, but flag generation routine is separated from input, so I just patched the binary to directly generate the flag and do int3, and loaded the driver via https://github.com/hfiref0x/TDL in vmware with VirtualKd. The flag was stored in +0x16390, and I patched +0x112AC with int3.

![image containing flag](flag.png)