# nomoreseacrypt

- ./chromeupdater: ELF64 which encrypts a file into temp.bin
- ./recovered_file.zip
  - temp.bin: An encrypted file

The binary utilizes C++ STL functions like string, so I assumed it was compiled with C++ compiler.

In summary, it does:

```c
rand_key() {
	srand(time(NULL))
	return ''.join(key[rand()%0x3e] for i in range(32))
}

if(getpwuid(geteuid())->pw_name=="buildmaster") {
	path = "$HOME" + "/src/charmony/lib/strangefinder/splinesreticulator.cpp"
	data = open(path, "rb").read()
	if(data.startswith("// Copyright 2019 - QwarkSoft")) {
		open("temp.bin", "wb").write(AES.new(
			rand_key(), MODE_CTR, counter=Counter.new(128, initial_value=0xe4b8c75accb877dab0f5a6f0a7aa0e67
		)))
	}
}
```

The encryption key is derived from timestamp seed, and it was similar from the specified timestamp from given temp.bin. I've attached solve.py which brute-forces some timestamp and gets the key, and decrypts the file.

## Some details on reverse engineering

C++ initializes global variable by utilizing `.init_array` in linux gcc. e.g. This binary uses 0x400af8 registered to `.init_array`:

```c
__int64 sub_400AF8()
{
...
  string::from_ptr(&qword_7C0800, "buildmaster");
  string::from_ptr(&off_7C07E0, "src/charmony/lib/strangefinder/splinesreticulator.cpp");
  string::from_ptr(&temp_bin, "temp.bin");
  string::from_ptr(&qword_7C07A0, "// Copyright 2019 - QwarkSoft");
...
}
```

The string object is usually 32 bytes with union field, but first two size_t fields are not union, so I define the structure like this:

```
00000000 str             struc ; (sizeof=0x20, mappedto_35)
00000000 buf             dq ?                    ; XREF: main+56/r
00000008 len             dq ?                    ; XREF: main+36/r
00000010 field_10        db 16 dup(?)            ; XREF: main+264/w
00000020 str             ends
```

In addition, you can add a breakpoint at 00000000004008CB to confirm that it uses AES sbox (rbp points it), and:

```c
  if ( byte_7BE130[0] == 0x72 )
  {
    result = 0LL;
    do
    {
      byte_7BE130[result] = ~byte_7BE130[result];
      ++result;
    }
    while ( result != 11 );
  }
  LOBYTE(result) = 1;
```

00000000004014EF both generates sbox and recovers Rcon table of AES. After seeing this, I tried to implement AES-CTR operation in pycrypto and it worked with same result, so I continued writing the solution code in python.

## Other links

- [libc FLIRT signatures](https://github.com/push0ebp/sig-database) to recover `time()`, `srand()`
- [ifstream example code](http://www.cplusplus.com/reference/fstream/ifstream/is_open/)
  - Useful when reversing 0000000000400763...00000000004007D0
- [Explanation about CTR mode operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR))
  - 401645 implements AES-CTR.
