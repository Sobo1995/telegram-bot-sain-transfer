
import os
import requests
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_TOKEN", "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI")
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    message = request.json.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    if chat_id:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={{
            "chat_id": chat_id,
            "text": "Бот амжилттай ажиллаж байна!"
        }})
    return "ok"

def set_webhook_once():
    try:
        webhook_url = "https://telegram-bot-sain-transfer.onrender.com/" + TOKEN
        api_url = "https://api.telegram.org/bot" + TOKEN + "/setWebhook"
        response = requests.post(api_url, data={{"url": webhook_url}})
        print("✅ Webhook auto-set status:", response.json())
    except Exception as e:
        print("❌ Failed to set webhook automatically:", e)

if __name__ == "__main__":
    set_webhook_once()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
