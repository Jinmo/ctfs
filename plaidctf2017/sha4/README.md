## SHA-4

This is web challenge, it has two forms, one inputs hex asn1, one inputs URL. asn1 for /comment, url for /upload. It was possible to leak a file via file:/// on /upload. Since it was apache server, I tried to get configuration for web server, and it worked.

file:///etc/apache2/sites-enabled/000-default.conf:

```xml
<VirtualHost *:80>
	ServerName sha4

	WSGIDaemonProcess sha4 user=www-data group=www-data threads=8 request-timeout=10
	WSGIScriptAlias / /var/www/sha4/sha4.wsgi

	<directory /var/www/sha4>
		WSGIProcessGroup sha4
		WSGIApplicationGroup %{GLOBAL}
		WSGIScriptReloading On
		Order deny,allow
		Allow from all
	</directory>

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
```

Yeah, /var/www/sha4/sha4.wsgi is the python source file.

/var/www/sha4/sha4.wsgi:

```python
import sys
sys.path.append("/var/www/sha4")

from server import app as application
```

Let's see /var/www/sha4/server.py, which is flask server source code file. (see src/ for leaked files)

```python
@app.route("/upload", methods=['POST'])
def upload():
  try:
    comment = urlopen(request.form['url']).read(1024*1024)
    open("/var/tmp/comments/%s.file"%hash(comment).encode("hex"), "w").write(comment)
    return comment
  except:
    return render_template_string(bad)
```

Aha! This part was for leaking files!

```python
bad     = """<h2>yo that comment was bad, we couldn't parse it</h2>"""
unsafe  = """<h2>that comment decoded to some weird junk</h2>"""
comment = """<h2>Thank you for your SHA-4 feedback. Your comment, %s, is very important to us</h2>"""

def is_unsafe(s):
  for c in s:
    # "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.:()?!-_'+=[]\t\n<>"
    if c not in (string.ascii_letters + string.digits + " ,.:()?!-_'+=[]\t\n<>"):
      return True
  return False

@app.route("/comments", methods=['POST'])
def comments():
  # skipped. bar is OctetString input.
  f = "/var/tmp/comments/%s.txt"%hash(ber).encode("hex")
  
  out_text = str(decode(ber))
  open(f, "w").write(out_text)

  if is_unsafe(out_text):
    return render_template_string(unsafe)

  commentt = comment % open(f).read()
  return render_template_string(commentt, comment=out_text.replace("\n","<br/>"))
```

Uh-oh. `commentt = comment % open(f).read()`, and `render_template_string` with it? It has template injection! However is_unsafe is sufficient for blocking `{` which is used by flask template engine (Jinja2). However look carefully, there is TOCTOU problem.

1. `open(f, "w").write(out_text)` writes out_text to the file.
2. `is_unsafe(out_text)` is checked.
3. Then the actual value used in template is read: `commentt = comment % open(f).read()`.

Hey, but the filename is sha4 hash and it makes a different content to saved on a different path..!

```python
f = "/var/tmp/comments/%s.txt"%hash(ber).encode("hex")
```

Right, right. Then this challenge becomes about the 2nd preimage attack to a custom hash algorithm using DES, which was trivial.



Hash algorithm below:

```python
def seven_to_eight(x):
  [val] = struct.unpack("Q", x+"\x00")
  out = 0
  mask = 0b1111111
  for shift in xrange(8):
    out |= (val & (mask<<(7*shift)))<<shift
  return struct.pack("Q", out)

def unpad(x):
  #split up into 7 byte chunks
  length = struct.pack("Q", len(x))
  sevens = [x[i:i+7].ljust(7, "\x00") for i in xrange(0,len(x),7)]
  sevens.append(length[:7])
  return map(seven_to_eight, sevens)

def hash(x):
  h0 = "SHA4_IS_"
  h1 = "DA_BEST!"
  keys = unpad(x)
  for key in keys:
    h0 = DES.new(key).encrypt(h0)
    h1 = DES.new(key).encrypt(h1)
  return h0+h1

```

hash(x) splits x to 7byte blocks, and with p64(length), it generates key with clearing MSBs (seven_to_eight generates MSB-cleared 8byte key with 7byte block). The attack vector is: **DES only uses 56bit key**. But DES implementations requires 8byte input. What's wrong?

The answer is: **It ignores every LSB of 8byte key**, making actual key as 56bit. However it clears every MSBs of it, so seven_to_eight doesn't stop us to make same hash values with different input. For example:

```python
c = os.urandom(8)
DES.new('\x01' * 8).encrypt(c) == DES.new('\x00' * 8).encrypt(c)

# Great example in http://stackoverflow.com/questions/23216138 .
DES.new('82514145').encrypt(c) == DES.new('93505044').encrypt(c)
```

OK, as a result, `hash('xx{{xxx'}}) == hash('xx[kxxx')`, `hash('xx}}xxx') == hash('xx]mxxx')`. With TOCTOU problem, we can exploit race condition with string w/ `{{` ~ `}}`, and `[k` ~ `]m`. For the rest part, see `solve.py` in this directory.