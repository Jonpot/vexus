"""
To test the flask server, this script will
send a POST request to the server https://74.109.242.11:5000/
"""

import requests
import json

url = "http://74.109.242.11:5000/"
data = {
    "name": "John",
    "age": 30
}

response = requests.post(url, json=data)

print(response.text)
print(response.status_code)

