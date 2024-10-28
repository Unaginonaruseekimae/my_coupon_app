from flask import Flask, request, redirect
import requests

app = Flask(__name__)

LINE_ACCESS_TOKEN = 'YOUR_LINE_ACCESS_TOKEN'
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'

@app.route('/')
def home():
    return 'Hello, Heroku!'

@app.route('/send_coupon', methods=['POST'])
def send_coupon():
    user_id = request.form.get('user_id')
    coupon_message = "Thank you for your review! Here is your coupon: XYZ123"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}',
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": coupon_message
            }
        ]
    }

    response = requests.post(LINE_API_URL, headers=headers, json=payload)
    return 'Coupon sent!' if response.status_code == 200 else 'Failed to send coupon'

if __name__ == '__main__':
    app.run(debug=True)
