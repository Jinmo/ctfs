from robobrowser import RoboBrowser
import time
from random import randint
from config import admin_id, admin_pw, domain
import logging


logging.basicConfig(filename='admin.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
l = logging.getLogger('admin')

"""
Fake admin script
repeat login!
sorry no javascript, no XSS
"""

while True:
    try:
        b = RoboBrowser(history=False)
        b.open('http://admin.'+domain)
        f = b.get_form()
        f['userid']=admin_id
        f['password']=admin_pw
        b.submit_form(f)
        time.sleep(3)
    except:
        time.sleep(3)
        continue

