## router

### 800. CityRouter

I found this router configuration utility listening on 0.0.0.0 in some city in Soviet Russia. Can it pwn you?

http://51.15.88.183:8080/

Binary: [router](router)

## Explanation

Analyzing the binary, I found that the http parser is probably from open source project, http-parser in nodejs by searching some strings used in the binary. So I skipped the HTTP-parsing part.

There is heap overflow vulnerability in JSON parser (which is not used in web interface), used in /admin POST request handler.
Usually JSON doesn't accept some control characters in input, but this program handles that differently (and unicode too).

The length used in string allocation determines the length by counting characters **before non-printable characters**.

```c
_DWORD *__fastcall json_parse_string(_BYTE *input, _BYTE *a2, _QWORD *a3)
{
...
  cur = input + 1;
  size = 0LL;
  while ( *cur != '"' && *cur > 31 && *cur != 127 && cur < a2 )
  {
    if ( *cur == '\\' )
      ++cur;
    ++size;
    ++cur;
  }
  if ( cur == a2 && *cur != '"' )
    return 0LL;
  ptr = calloc(1uLL, size + 1);
```

But when actually decoding & copying JSON strings to the new buffer, it doesn't check if it's non-printable. It just checks if `*cur` is '"', and even '\x00' is accepted as input, and copied, too.

Since a json object can contain multiple key value & pair, we have a primitive like this:

```
char *ptr = calloc(1, controlled_size);
memcpy(ptr, input, controlled_size_2);
```

The fun thing is, when the parser meets some invalid condition for a JSON object, like, the value is object, it frees key and returns NULL. Then it continues parsing after ignoring the previous chracters. This was useful when doing some heap feng-shui, by allocating key, key string object(0x20 size), and free-ing both of it.

## Exploitation

FYI, it's NX-enabled, non-PIE binary, with partial RELRO. The server is fork-and-accept concept, so there is ASLR but the address is fixed between executions.

Corrupting fastbin is one of easiest techniques in ptmalloc exploitation. Since there were a useful and fixed bytes(0x7f[^1]) in .got.plt which is writable, I looked some variables in .data (it's after .got.plt) and found some usages. There were format string used when making a HTTP response. We can make an arbitrary-sized overflow, so we can simply choose last .got.plt entry as fake chunk and make malloc return that address.

The process of the trick is like this.

```c
#define FASTBIN_SIZE 0x60
char target = {0x41, 0x41, 0x41, 0x41, 0x41, 0x7f, 0, 0, 0, 0, 0, 0, 0}; // 0x41 can be arbitrary bytes since it's not used. In this case, .got.plt.
void **a = malloc(FASTBIN_SIZE);
free(a);
*a = target + 5 - 8; // corrupt chunk->fd
malloc(FASTBIN_SIZE);
assert(malloc(FASTBIN_SIZE) == target + 5 + 8);
```

We should know the target's pointer when attacking through this technique, but we know it's around .got.plt.

For corrupting fd pointer we can use heap overflow (value to change is marked with \*):

```
--------------------------------------------
| string to overflow ....... | size | *fd* |
--------------------------------------------
```

There is no need to change the next chunk's size field.

So we'll place a freed fastbin chunk with size 0x60 ~ 0x67. If the size differs from the value on target + 5, it will raise error "memory corruption (fast)". Let's see what happens in heap for each cases in parser:

### 1. "%s": {...

It's like:

```
// json_parse_key_value -> json_parse_string
char *s = malloc(size);
memcpy(s, input, size2);
string *ptr = malloc(32);
// ptr->buf = s;
// ptr->type = STRING;
return ptr;

// The program returns to json_parse_key_value
// What? {}?
free(s);
free(ptr);
return NULL;

```

As mentioned above the parser just ignores the key-value pair and continues parsing. The JSON below is still valid.

```json
{
  "key": a
  "key2": 1
}
```

### 2. "%s": "%s" (normal json)

```
char *s = malloc(size);
memcpy(s, input, size2);
string *ptr = malloc(32);
return ptr;

keyvalue *kv = malloc(16);
kv->key = key;
```

It's like a puzzle! My solution is, on the second post. [link](second.md)

[^1]: which is 0x78 | PREV_INUSE | NON_MAIN_ARENA | IS_MMAPPED. Doesn't matter when obtaining controlled address with malloc.