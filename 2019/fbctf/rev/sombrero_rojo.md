# Sombrero Rojo

## Part 1

```
The binary has two flags, submit the other flag to the part 2.
```

I was given a file which was ELF format. main() checks argv[1] and prints a fake flag if password is matched. There is another function pointed by .init_array, and it does this:

- ptrace(PTRACE_TRACEME) == -1 -> just return (anti debugging)
- Opens /tmp/key.bin and checks if `key[0] == -5 && key[2] == -107 && key[3] == 23 && key[4] == -112 && key[5] == -12`
- Print the part1 flag
- Decrypts another ELF binary and writes next_challenge.bin to cwd.

You can make a /tmp/key.bin with the content above to get part 1 flag.

```
$ echo -ne '\xfb_\x95\x17\x90\xf4' > /tmp/key.bin
$ ./sombrero_rojo a
fb{7h47_W4sn7_S0_H4Rd}
Ready for the next challenge?... press enter
```

## Part 2

```
Once you get the flag for part 1, go get the flag for part 2. Note that the developer isn't a great programmer, so watch out for bugs.
```

There is a off-by-one error (yes, I analyzed the whole routine and guessed) when decrypting the embedded binary with SHA256+RC4. In 0x402E00:

```
.text:0000000000402FF8                 movdqu  xmm0, xmmword ptr [rdi+0Eh]
.text:000000000040300E                 movdqu  xmm0, xmmword ptr [rdi+1Eh]
```

The key is scheduled at rdi+0xD, rdi+0x1D, so after patching the binary at runtime, next_challenge.bin becomes an ELF file.

