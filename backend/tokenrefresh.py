import requests
import json

with open('/etc/config.json') as file:
    config = json.load(file)

email = config.get('AMMA_EMAIL')
password = config.get('SHIPROCKET_API_AMMA_PASS')
url = "https://apiv2.shiprocket.in/v1/external/auth/login"

payload = json.dumps({
  "email": email,
  "password": password
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

token = json.loads(response.text)

config['SHIPROCKET_TOKEN'] = str(token['token'])
with open('/etc/config.json','w') as f:
    json.dump(config, f, indent=2)


