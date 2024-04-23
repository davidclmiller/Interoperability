import requests

BASE = " http://127.0.0.1:5000/"
APP_VERSION = "v1/"

response = requests.get(BASE + APP_VERSION + "data/0")
print(response.json())
