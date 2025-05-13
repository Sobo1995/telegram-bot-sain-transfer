
import os
import requests
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_TOKEN", "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI")
API_URL = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_URL = f"https://telegram-bot-sain-transfer.onrender.com/{TOKEN}"

app = Flask(__name__)

def set_webhook_once():
    try:
        res = requests.post(f"{API_URL}/setWebhook", data={"url": WEBHOOK_URL})
        print("✅ Webhook auto-set:", res.json())
    except Exception as e:
        print("❌ Webhook error:", e)

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    return requests.post(f"{API_URL}/sendMessage", json=data)

def get_fee(tugrug):
    try:
        amount = int(tugrug)
        if amount <= 100000:
            fee = 3000
            yuan_fee = 30
        elif amount <= 1000000:
            fee = 5000
            yuan_fee = 50
        elif amount <= 2000000:
            fee = 5000
            yuan_fee = 100
        elif amount <= 5000000:
            fee = 10000
            yuan_fee = 100
        elif amount <= 10000000:
            fee = 20000
            yuan_fee = 100
        else:
            fee = 25000
            yuan_fee = 100
        return f"💱 {amount:,}₮ → Шимтгэл: {fee:,}₮ + {yuan_fee}¥ → {(amount - fee) / 462:.2f}¥"
    except:
        return "Ойлгосонгүй. Та зөвхөн тоон дүн оруулна уу."

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    msg = request.json.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text", "").lower()

    if not chat_id or not text:
        return "ok"

    if text in ["/start", "menu", "меню", "эхлэх"]:
        keyboard = {
            "inline_keyboard": [
                [{"text": "📋 Гуйвуулгын форм", "callback_data": "form"}],
                [{"text": "📈 Ханш", "callback_data": "rate"}],
                [{"text": "💸 Шимтгэл", "callback_data": "fee"}],
                [{"text": "📄 Бичиг баримт", "callback_data": "docs"}],
                [{"text": "ℹ️ Бидний тухай", "callback_data": "about"}]
            ]
        }
        send_message(chat_id, "Та доорх цэснээс сонгоно уу:", reply_markup=keyboard)
    elif any(x in text for x in ["ханш", "hansh"]):
        send_message(chat_id, "📈 Манай ханш: 1 юань = 462₮")
    elif any(x in text for x in ["шимтгэл", "shimtgel"]):
        send_message(chat_id, "💡 Шимтгэл:
1¥ - 1,000¥ = 3,000₮
1,000¥ - 10,000¥ = 5,000₮
10,000¥+ = 10,000-25,000₮")
    elif any(x in text for x in ["утас", "dugaar", "utas"]):
        send_message(chat_id, "📞 Утас: 80908090")
    elif any(x in text for x in ["данс", "дансны дугаар", "bank", "dans"]):
        send_message(chat_id,
            "💳 Дансны дугаарууд:
"
            "Хаан банк: 5077407759
"
            "ХХБ: 431004884
"
            "Голомт: 3635112076
"
            "Төрийн банк: 343200497501
"
            "Хас банк: 5002742902")
    elif any(x in text for x in ["бичиг баримт", "document", "barimt"]):
        send_message(chat_id,
            "📄 Бүрдүүлэх бичиг баримт:
"
            "• Илгээгч, хүлээн авагчийн бичиг баримт (зураг)
"
            "• Хүлээн авагчийн банкны нэр, данс
"
            "• Гүйлгээний утга, шаардлагатай бол гэрээ")
    elif any(x in text for x in ["бидний тухай", "about", "bidnii"]):
        send_message(chat_id,
            "🏢 **Бидний тухай**
"
            "Бид хамгийн сүүлийн үеийн технологи ашиглан юанийн гуйвуулгыг цахимжуулсан. "
            "7 дахь жилдээ амжилттай ажиллаж байна.

"
            "🎯 **Алсын хараа**: Оюунлаг ирээдүйг дэмжинэ.
"
            "🔒 **Эрсдэлгүй**
📑 **Албан ёсны**
⚡ **Хурдан**
🔁 **Уян хатан**")
    elif text.replace(",", "").replace("₮", "").strip().isdigit():
        send_message(chat_id, get_fee(text.replace(",", "").replace("₮", "").strip()))
    else:
        send_message(chat_id,
            "🤖 Та 'ханш', 'шимтгэл', 'данс', 'утас', 'бичиг баримт', 'бидний тухай' зэрэг түлхүүр үг оруулж болно. "
            "Мөн тоон дүн оруулбал шимтгэлийг тооцно.
/menu гэж бичиж цэс гаргана уу.")
    return "ok"

if __name__ == "__main__":
    set_webhook_once()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
