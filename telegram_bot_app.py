
from flask import Flask, request
import os
import requests

app = Flask(__name__)

BOT_TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
WEBHOOK_SECRET_PATH = f"/{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

@app.route(WEBHOOK_SECRET_PATH, methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].lower()

        if "шимтгэл" in text:
            send_message(chat_id, "\U0001F4B0 Шимтгэлийн шатлал:\n1¥ - 1,000¥ = 3,000₮\n1,000¥ - 10,000¥ = 5,000₮\n10,000¥+ = 10,000-25,000₮")
        else:
            send_message(chat_id, "Таны асуултыг ойлгосонгүй. Та 'шимтгэл' гэж бичнэ үү.")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
