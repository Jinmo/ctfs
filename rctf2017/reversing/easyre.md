## easyre

First, run this command since this binary seems packed in upx-like routine. It worked.

```shell
$ upx -d ./easy_re
```

Secondly, it opens a pipe, forks a process, child process sends a string to the pipe, parent process receives it, and does some string manipulation. The routine that shows the flag has some unsatisfiable condition (1 == 0). I binary patched it.

```asm
In IDA Pro,

.text:080486AD                 mov     [ebp+var_D], al
.text:080486B0                 mov     [ebp+var_C], 1  ; Keypatch modified this from:
.text:080486B0                                         ;   mov [ebp+var_C], 0
.text:080486B7                 cmp     [ebp+var_C], 1
```

Then run the command.

```shell
$ echo|./easy_re

OMG!!!! I forgot kid's id
Ready to exit     

You got the key
 rhelheg
```