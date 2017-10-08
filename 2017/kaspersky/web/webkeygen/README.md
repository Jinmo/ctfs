## Challenge

### 700. web keygen

crackme! http://95.85.55.168/vmctf.html

## Explanation

The [webpage itself](challenge/vmctf.html) contains an obfuscated x86-like virtual machine, and the code for it.
I ported the javascript VM as a disassembler in python, and translated it to x86, and compiled it.
Then in IDA Pro, I found it was crc32, with initialization value 0x12345678.

I could use crc32 reverse code in internet, but the password was 8byte. It has probability with 1/2^32.

However after verifying password, it does xor-decoding with 8-byte password and the encrypted flag.

Since the flag starts with 'KLCTF', I could guess the first 4byte of password as 'KLCT'^ciphertext[:4].

Then it only has one solution. "8XcCDUhG". Supplying the password to the webpage, I could get the flag.

**KLCTF7B0AEB2426A8F829276C73A32241ADBA**