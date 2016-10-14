import requests

s = requests.Session()

r = s.get('http://challenges.hackover.h4q.it:8202/')
url = r.url
license = url.split('=')[1]
m0, m1 = 'A' * 16, 'A' * 16
r = s.post('http://challenges.hackover.h4q.it:8202/ciphertext?m0=%s&m1=%s&driver_license=%s' % (m0, m1, license))
text1 = r.text
#m0 = 'B' * 8
r = s.post('http://challenges.hackover.h4q.it:8202/ciphertext?m0=%s&m1=%s&driver_license=%s' % (m0, m1, license))
text2 = r.text
print `text1`, `text2`