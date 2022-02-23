from flask import request

import requests

req = requests.get("https://randomuser.me/api")

print(req.content)

req.text