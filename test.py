# 0731ecf2d553d9d66621fbafe1946fa5e2e116b1cc08d37b049f98fac425839e

# Importing Library
import requests
import json

# Creating Link
link = 'http://127.0.0.1:5000/'
api_key = '0731ecf2d553d9d66621fbafe1946fa5e2e116b1cc08d37b049f98fac425839e'

# posting a get request
response = requests.get(link+'api='+api_key+'/allanime')
data = json.loads(response.text)
for i in data[:100]:
    print(i)