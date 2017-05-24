# crackme

The given binary performs

1. the RC6-variant block-cipher encryption with input with fixed key
2. xors with some md5 hashes,
3. then compares it with fixed, hardcoded value.
 
If the text is correct, it prints the flag.
 
Script for (2): `./preprocess.py` .
Source code for (1): `./rc6.c` (`./rc6` is compiled binary)