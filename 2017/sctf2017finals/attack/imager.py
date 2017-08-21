#!/usr/bin/env python3
''' flag file is '/'.join(__file__.split('/')[:-1]) + '/flag' '''

# 풀이는 상당히 간단합니다. secret_key가 있으면 세션을 맘대로 생성할 수 있으므로 http:// 부분을 file:///로 바꾸고 세션을 생성해준 다음에 그 세션 쿠키값을 서버에 그대로 넘겨주면 됩니다.
# 플래그: SCTF{3a5y_e4zy_p1ckl1ng}

from flask import Flask
from flask import Response
from flask import request, session
from flask import url_for, redirect
from flask import render_template, flash

from bs4 import BeautifulSoup as bs
from base64 import b64encode
from pycurl import Curl
from io import BytesIO
import imghdr


# init app
app = Flask(__name__)
app.secret_key = 'v3ry_v3ry_s3cr37_k3y'


# utils
def curl(url):
    io = BytesIO()
    c = Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, io)
    c.perform()
    c.close()
    res = io.getvalue()
    io.close()
    return res


def gen_base64(tag):
    src = tag.get('src')
    if src is not None:
        data = curl(src)
        img_type = imghdr.what(None, h=data)
        if img_type is not None:
            encode = b64encode(data).decode('ascii')
            tag['src'] = 'data:image/{};base64,{}'.format(img_type, encode)


# routing
@app.route('/', methods=['POST', 'GET'])
def main():
    url = request.form.get('url')
    if url is not None:
        session['url'] = 'file:///{}'.format(url)
        return redirect(url_for('convert'))
    return render_template('main.html')


@app.route('/convert')
def convert():
    try:
        target = session.get('url')
        if target is None:
            return url_for('main')
        else:
            r = curl(target)
            soup = bs(r, 'html.parser')
            imgs = soup.find_all('img')
            list(map(gen_base64, imgs))
            return Response(soup.prettify(), mimetype='text/plain')
    except:
        flash('invalid url')
        return redirect(url_for('main'))


@app.route('/get_source')
def get_source():
    with open(__file__, 'r') as f:
        res = f.read()
    return Response(res, mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=17711)
