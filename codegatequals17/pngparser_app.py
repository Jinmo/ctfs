import sys, traceback, tempfile, os, urllib2, base64
from subprocess import Popen, PIPE
from flask import Flask, render_template, request

app = Flask(__name__)

@app.errorhandler(404)
def page_not_fount(e):
    return render_template('error.html', error=e), 404


@app.errorhandler(500)
def internal_error(e):
    trace = traceback.format_exc()
    return render_template('error.html', error=e, message=trace), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fileupload', methods=['POST'])
def fileupload():
    file = request.files['upload_file']
    if not file:
        return render_template('result.html', result="Invalid Input ~.~")

    png_data = file.read()
    png_img = base64.b64encode(png_data)
    out = parser_run(png_data)

    return render_template('result.html', png_img=png_img, result=out)

@app.route('/url', methods=['POST'])
def url():
    protocol = request.form['protocol']
    url = request.form['url']
    if not protocol or not url:
        return render_template('result.html', result="Invalid Input ~.~")

    addr = protocol + url
    req = urllib2.urlopen(addr, timeout=1)
    png_data = req.read()
    png_img = base64.b64encode(png_data)
    out = parser_run(png_data)

    return render_template('result.html', png_img=png_img, result=out)

def parser_run(png_data):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(png_data)
    f.close()

    args = "./PNGParser %s" %(f.name)
    proc = Popen(args, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    out, err = proc.communicate()
    os.unlink(f.name)
    return out


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "[Usage] %s port" %sys.argv[0]
        sys.exit(0)

    try:
        port_num = int(sys.argv[1])
    except ValueError:
        print "[Usage] port is only number : %s" %sys.argv[1]

    app.run(host='0.0.0.0', port=port_num, threaded=True)