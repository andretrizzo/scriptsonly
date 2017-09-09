import requests
import json
import base64
import yaml
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

with open("pydata.yaml", 'r') as stream:
    try:
        pydata = yaml.load(stream)
        ip_addr = pydata['ip_addr']
        username = pydata['username']
        password = pydata['password']
        command = pydata['command']
    except yaml.YAMLERROR as exc:
        print(exc)


url = 'http://' + ip_addr + '/rest/v3/'
creds = {'userName': username, 'password': password}

s = requests.Session()
r = s.post(url + 'login-sessions', data=json.dumps(creds), timeout=1)
cookie_response = r.json()['cookie']
if r.status_code != 201:
    print('Login error, status code {}'.format(r.status_code))


cookie = {'cookie': cookie_response}
c = {'cmd': command}
post_command = requests.post(url + 'cli', headers=cookie, data=json.dumps(c), timeout=1)



if post_command.status_code != 200:
    print(('Error, status code {}'.format(post_command.status_code)))
else:
    print('Status Code: ' + str(post_command.status_code))
    response = post_command.json()['result_base64_encoded']
    decoded_r = base64.b64decode(response).decode('utf-8')
    print(decoded_r)

