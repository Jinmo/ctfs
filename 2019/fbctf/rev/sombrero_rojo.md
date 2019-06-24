# Sombrero Rojo

## Part 1

```
The binary has two flags, submit the other flag to part 2.
```

I was given a file which was ELF64 format. First I looked at main() with a decompiler tool.
(renamed some functions after analyzing each function)

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  flag_content[0] = 0x43424E3954464926;
  a1[0] = 0x591A573C5A466054;
  ...
  flag_content[3] = 0x413BFA534C2E0808;
  a1[2] = 0x4B59175E0B0B2757;
  if ( argc == 2 )
  {
    decrypt_string(flag_content);               // just adds strlen
    decrypt_string(a1);
    if ( strcmp(a1, argv[1]) )
    {
      __printf_chk(1, "Hmmm...");
      puts("Try again!");
      exit(1);
    }
    __printf_chk(1, "%s{%s}\n", flag_prefix, flag_content);
  }
  return 0;
}
```

Since argv[1] is compared with hardcoded string without any transformation, we can just set a breakpoint before strcmp, and extract the expected value. Let's do it. Since ELF is modified a bit so gdb cannot load it, we can patch the binary to loop infinitely just before strcmp, and attach to it, since gdb doesn't check ELF's validity when debugging already running process.

```
Patch:
0000000000400A92    E8 01     -> EB FE 

$ ./sombrero_rojo test
$ sudo gdb -p `pgrep sombrero|tail -1`
Attaching to process 15145
Could not attach to process.  If your uid matches the uid of the target
process, check the setting of /proc/sys/kernel/yama/ptrace_scope, or try
again as the root user.  For more details, see /etc/sysctl.d/10-ptrace.conf
warning: process 15145 is already traced by process 15129
...
```

Oops, it seems like there is an anti-debugging techniques. To make ptrace fail, a process can do PTRACE_TRACEME itself, since only one process can debug a target process. Seems like the program did it before main(), so let's see .init_array at 0x6bb138.

```
.init_array:00000000006BB138 funcs_405710    dq offset sub_4010A0    ; DATA XREF: sub_4056D0+2↑o
.init_array:00000000006BB138                                         ; sub_4056D0+B↑o ...
.init_array:00000000006BB140                 dq offset sub_4005A0
.init_array:00000000006BB148                 dq offset sub_400B20
```

TL;DR. sub_4005a0 has some suspicious routines, and sub_44ec50 is ptrace. Let's just set rax to -1 to debug main().

```
Patch:
000000000040060C    E8 3F E6 04 00     -> push -1; pop rax; nop; nop

$ ./sombrero_rojo test
$ sudo gdb -p `pgrep sombrero|tail -1`
0x0000000000400a92 in ?? ()
gef➤  x/s $rdi
0x7ffc5074cd70: "my_sUp3r_s3cret_p@$$w0rd1"
gef➤  x/s $rsi
0x7ffc5074d262: "test"
```

Let's revert the patches and execute the binary with the password above ($rdi).

```
$ ./sombrero_rojo 'my_sUp3r_s3cret_p@$$w0rd1'
Nope{Lolz_this_isnt_the_flag...Try again...}
```

It prints a fake flag if password is matched. Since there is another function (sub_4005a0) pointed by .init_array, I analyzed the routine with decompiler. It does this:

- ptrace(PTRACE_TRACEME) == -1 -> just return (anti debugging)
- Opens /tmp/key.bin and checks if `key[0] == -5 && key[2] == -107 && key[3] == 23 && key[4] == -112 && key[5] == -12`
- Print the part1 flag
- Decrypts another ELF binary and writes `next_challenge.bin` to cwd. (part2)

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

Part 2 is started after 0x40091b prints the flag above. As a result, next_challenge.bin is created and executed with execve. I kept reading the code over and over with decompiler. After that I guessed it was SHA256+RC4 encryption scheme.

```c
// bad sp value at call has been detected, the output may be wrong!
__int64 __fastcall sub_402E00(int *a1, __int64 a2, __int64 a3)
{
...
  while ( *(_BYTE *)v30 == 0xFB )
  {
    v30 = (__int64 *)((char *)v30 + 1);
    if ( &v81 == v30 )
    {
      // Some complex key-scheduling routines here
      ...
      // <-- 1
      *(__m128i *)((char *)a1 + 13) = _mm_loadu_si128((const __m128i *)&v79);
      *(__m128i *)((char *)a1 + 29) = _mm_loadu_si128((const __m128i *)&v80);
      break;
    }
  }
  // <-- 2 at 0000000000402FF8, 000000000040300E
  v99 = _mm_loadu_si128((const __m128i *)((char *)a1 + 14));
  v100 = _mm_loadu_si128((const __m128i *)((char *)a1 + 30));

```

After looking `<-- 1` and `<-- 2`, I suspected that there is a off-by-one error when decrypting the embedded binary with SHA256+RC4. In 0x402FF8:

```
.text:0000000000402FF8                 movdqu  xmm0, xmmword ptr [rdi+0Eh]
.text:000000000040300E                 movdqu  xmm0, xmmword ptr [rdi+1Eh]
```

The binary schedule decryption keys at rdi+0xD, rdi+0x1D, so after patching the binary at runtime, next_challenge.bin becomes an ELF file.

```
Patch:
0000000000402FFC    0E     -> 0D 
0000000000403012    1E     -> 1D 

$ ./sombrero_rojo
fb{7h47_W4sn7_S0_H4Rd}
Ready for the next challenge?... press enter
$ file ./next_challenge.bin
./next_challenge.bin: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=55b454a63bd0e6786b9ee13c123ccde747ce3c30, not stripped
$ ./next_challenge.bin
...
fb{YOU GOT THE LAST FLAG!!! NICE WORK!!!}
```

It was a bit guessy, but anyway it worked!
