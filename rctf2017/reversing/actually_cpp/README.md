# actually cpp

It’s a CrossBridge-compiled swf file, with AES-CBC encryption + brainf\**k interpreter with fixed code. There were “check” routine, which was called in Console class. The routine’s statement was like x86 assembly. I reversed the routine, then I found that the key is hardcoded, and before encrypting, the key and iv is modified by a fixed brainf\**k code. IV, key = buf[:16], buf[16:]

```
>>>>>+++++<<<<----->>>++<<<<<<<<<-----
```

Since the output buffer’s offset was initially set to 16, it’s like this.

```py
key[21] += 5
key[17] -= 5
key[20] += 2
key[11] -= 5
```

Full solution code is in `actually_cpp.py` .