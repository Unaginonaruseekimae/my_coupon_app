from flask import Flask, redirect
import os
import requests
import pandas as pd

app = Flask(__name__)

# LINEアクセストークン
LINE_ACCESS_TOKEN = "YOUR_LINE_ACCESS_TOKEN"
# レビューURL
REVIEW_URL = "https://g.page/r/CWjQxOIQzuUzEBM/review"
# ユーザーIDを含むCSVファイルのパス
USER_ID_CSV_PATH = "user_ids.csv"

def send_coupon(user_id):
    """指定したユーザーIDにクーポンメッセージを送信する関数"""
    message = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": "クーポンが発行されました！お楽しみください！"
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=message)
    return response.status_code == 200

@app.route('/review', methods=['GET'])
def review():
    # ユーザーIDをCSVから取得
    df = pd.read_csv(USER_ID_CSV_PATH)
    user_ids = df.iloc[:, 0].tolist()  # 1列目のユーザーIDを取得

    # クーポンを送信
    for user_id in user_ids:
        send_coupon(user_id)

    # レビューリンクにリダイレクト
    return redirect(REVIEW_URL)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
