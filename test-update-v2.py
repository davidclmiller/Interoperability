import requests

BASE = " http://127.0.0.1:5000/"
APP_VERSION = "v1/"

data = [{'wtemp': 78, 'wdescription': "clear", 'currency': 988, 'brewname': "testpub", 'brewurl': "http:www.test.com", 'brewphone': "4444444444"}]
for i in range(len(data)):
    response = requests.patch(BASE + APP_VERSION + "data/0" + str(i), data[i])
    print(response.json())

input()
response = requests.patch(BASE + APP_VERSION + "data/2")
print(response.json())