import requests

BASE = " http://127.0.0.1:5000/"
APP_VERSION = "v1/"

data = [{'wtemp': 78, 'wdescription': "clear", 'currency': 988, 'brewname': "testpub", 'brewurl': "http:www.test.com", 'brewphone': "55555555555"}]
for i in range(len(data)):
    response = requests.put(BASE + APP_VERSION + "data/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + APP_VERSION + "data/2")
print(response.json())