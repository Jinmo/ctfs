#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from flask import Flask,request,Response
from flask import render_template, flash
from hashlib import md5
import random, string
import time
import sys
import logging

# Get configuration for challenge setup
from config import admin_id, admin_pw, flag, domain, front_port, back_port, check_apikey

logging.basicConfig(filename='backend.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
l = logging.getLogger('backend')

app = Flask(__name__)
db = {}
login = time.time()

@app.route('/', subdomain='admin', methods=['GET', 'POST'])
def serve_admin():
    global login
    userid = request.form.get('userid') or None
    password = request.form.get('password') or None
    if userid and password:
        if userid == admin_id and password == admin_pw:
            login = time.time()
            flash("Welcome, flag is "+flag)
        else:
            flash("Failed")
    return render_template('admin.html', last_login = int(time.time()-login))

@app.route('/', methods=['GET', 'POST'])
def serve_main():
    page = request.form.get('page') or None
    cache = (request.form.get('cache') == 'on') or False
    apikey = request.form.get('apikey') or None
    link = None
    if apikey and check_apikey(apikey):
        subdomain = apikey[:16]
        if page:
            if len(page) > 10000: # Not much memory ;(
                flash('Page size too large')
            else:
                db[subdomain] = (page, cache)
                link = 'http://%s.%s/'%(subdomain,domain)
                flash('Success!')
    elif page:
        flash('Invalid API key')

    return render_template('main.html', link=link)

@app.route('/', subdomain='<subdomain>', methods=['GET'])
def serve_site(subdomain):
    if subdomain not in db:
        return ('Domain Not Found', 404)
    page, cache = db[subdomain]
    host = request.host
    if cache:
        return (page, {'Save-Cache':'1'})
    else:
        return page

if __name__ == '__main__':
    app.config['SERVER_NAME'] = domain 
    app.secret_key=''.join(random.choice(string.printable) for _ in range(32))
    app.run( host='127.0.0.1',port=back_port, threaded=True, debug=False)

