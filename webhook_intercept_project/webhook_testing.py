"""
Goal of this project:
to see if I can intercept a discord webhook from Dicecloud.com, 
check it for certain keywords, then continue to let it ride
to its intended destination.

Idea:
- Replace the webhook URL on Dicecloud with my own at jonpot.com
- TESTING: See if I can just recieve the webhook and put it on a webpage

Method:
- Use Flask to create a simple server
- Have the server listen for POST requests
- Generate an html page that displays the POST data
"""

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    return jsonify({"status": "success"}), 200

@app.route('/')
def home():
    return "<h1>Webhook Testing</h1>", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)