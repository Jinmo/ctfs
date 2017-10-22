# HelloDalvik
The application has 2 flag-related class: MathMethod, MainActivity. MathMethod has 5 functions: `MathMethod[0-5](int x, int y)`. The role of each function is:

```
1: x + y
2: x * y
3: x % y
4: x / y
5: x ^ y
```

MainActivity calls native method named stringFromJNI(). Unlike the method name, it modified dalvik code for MathMethod_1, MathMethod_4. So the role changes to:

```
1: x % y
2: x * y
3: x % y
4: x + y
5: x ^ y
```

Then the MainActivity registers click handler for a button, which encrypts the content of a textbox, 3 bytes for each block. It compares the ciphertext with hardcoded value.
Since the block size is not so large(len(charset)^3), I just created all combinations for a block and the corresponding ciphertext block. It was n:1 encryption so some encrypted flag had more than one case. I just tried all combinations for the flag.

Routine of `MainActivity` class is in `hellodalvik.java` (decompiled with jadx).
 
Solution code is `hellodalvik.py`.