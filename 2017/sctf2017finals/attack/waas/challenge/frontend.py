#!/usr/bin/python3
from http.server import *
from http.client import *
from urllib.parse import unquote_plus
from socketserver import ThreadingMixIn
import time
import sys
import logging

# Get configuration for challenge setup
from config import blacklist, admin_ip, domain, front_port, back_port

logging.basicConfig(filename='frontend.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
l = logging.getLogger('frontend')
cache = {}
no_cache = []
cache_timeout = 5 # 5 seconds


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class Handler(BaseHTTPRequestHandler):
    req_data = b'' #request
    res_data = b'' #response
    def forward(s):
        l.info('Forwarding %s %s %s'%(s.host, s.command, s.path))
        c = HTTPConnection('localhost', back_port, timeout=5)
        c.putrequest(s.command, s.path, skip_host=True, skip_accept_encoding=True)
        for (h,v) in s.headers.items():
            c.putheader(h, v)
        c.putheader("X-Forwarded-For",s.client_address[0])
        if 'Content-Length' in s.headers:
            s.req_data = s.rfile.read(int(s.headers['Content-Length']))
            c.endheaders(s.req_data)
        else:
            c.endheaders()
        r = c.getresponse()
        c.close()
        return r

    def firewall(s):
        if ('admin' in s.host) and (s.client_address[0] not in admin_ip):
            return "Permission Denied. Admin Only"
        for v in blacklist:
            if v in s.host.lower(): # domain blacklist
                return "Domain %s is blocked" % s.host
            if (v in unquote_plus(s.req_data.decode().lower())): # keyword blacklist
                return "Bad request: %s" % v
            if (v in s.res_data.decode().lower()): # keyword blacklist
                return "Bad response: %s" % v
        return None
    
    def send_res(s, status, headers):
        err = s.firewall()
        if err:
            l.warning("Firewall "+err)
            s.send_response(403)
            s.end_headers()
            s.wfile.write(err.encode())
            return
        s.send_response_only(status)
        for (h,v) in headers:
            s.send_header(h, v)
        s.end_headers()
        s.wfile.write(s.res_data)
    
    def send_cache(s):
        if (s.host in no_cache) or (s.host not in cache):
            return False
        status, headers, data, timeout = cache[s.host]
        if timeout < time.time(): # timeout
            cache.pop(s.host)
            return False
        l.info('Cached %s %s %s'%(s.host, s.command, s.path))
        s.res_data = data
        s.send_res(status, headers)
        return True
        
    def get_host(s):
        host = None
        for (h,v) in s.headers.items():
            if h.lower().strip() == 'host':
                host = v.lower()
        return host
    
    def do_POST(s):
        s.do_GET(skip_cache=True)

    def do_GET(s, skip_cache=False):
        s.host = s.get_host()
        if s.host == None:
            s.send_response(400)
            s.end_headers()
            return
        if not skip_cache and s.send_cache():
            return # cache send success
        # s.host Host:
        # GET http://qwefiui2vuopi1um13v5.sctfwaas.com.com:8080/ HTTP/1.1
        # Host: admin.sctfwaas.com:8080
        r = s.forward()
        headers = r.getheaders()
        s.res_data = r.read()
        if r.getheader('Save-Cache', False):
            cache[s.host] = (r.status, headers, s.res_data, time.time()+cache_timeout)
        s.send_res(r.status, headers)
        s.close_connection = True


if __name__ == '__main__':
    no_cache.append(domain) # do not cache main page
    httpd = ThreadingHTTPServer(('0.0.0.0', front_port), Handler)
    httpd.serve_forever()
