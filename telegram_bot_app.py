
import os
import re
import requests
from flask import Flask, request

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
BOT_URL = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_URL = f"https://telegram-bot-sain-transfer.onrender.com/{TOKEN}"

app = Flask(__name__)

user_states = {}
user_data = {}
form_questions = [
    "1. Хүлээн авагчийн нэр?",
    "2. Банкны нэр?",
    "3. Дансны дугаар?",
    "4. Илгээгчийн нэр?",
    "5. Утасны дугаар?",
    "6. Гүйлгээний утга?",
    "7. Бичиг баримт (зураг, файл) илгээнэ үү:"
]

def set_webhook():
    try:
        res = requests.post(f"{BOT_URL}/setWebhook", data={"url": WEBHOOK_URL})
        print("✅ Webhook set:", res.json())
    except Exception as e:
        print("❌ Webhook error:", e)

def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{BOT_URL}/sendMessage", json=payload)

def normalize_input(text):
    replace_map = {
        "hansh": "ханш", "shimtgel": "шимтгэл", "barimt": "баримт", "bichig": "бичиг",
        "tuhai": "тухай", "bidnii": "бидний", "guivuulga": "гуйвуулга", "utas": "утас",
        "dans": "данс", "dugaar": "дугаар", "form": "/form", "menu": "/start"
    }
    for latin, cyrillic in replace_map.items():
        text = re.sub(rf"\b{latin}\b", cyrillic, text)
    return text

def calculate_fee(amount):
    amount = int(amount)
    if amount <= 100000:
        fee, yuan = 3000, 30
    elif amount <= 1000000:
        fee, yuan = 5000, 50
    elif amount <= 2000000:
        fee, yuan = 5000, 100
    elif amount <= 5000000:
        fee, yuan = 10000, 100
    elif amount <= 10000000:
        fee, yuan = 20000, 100
    else:
        fee, yuan = 25000, 100
    net = amount - fee
    rate = 462
    return f"💱 {amount:,}₮ → Шимтгэл: {fee:,}₮ + {yuan}¥ → {net // rate}¥ орчим"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.json
    message = update.get("message") or {}
    callback = update.get("callback_query")

    if message:
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]
        text = message.get("text", "")
        normalized = normalize_input(text.lower())

        if user_id in user_states:
            step = user_states[user_id]
            if step < len(form_questions) - 1:
                user_data.setdefault(user_id, {})[f"q{step+1}"] = text
                user_states[user_id] += 1
                send_message(chat_id, form_questions[user_states[user_id]])
            else:
                if "document" in message or "photo" in message:
                    send_message(chat_id, "✅ Бүх мэдээлэл бүртгэгдлээ. Баярлалаа!")
                    user_states.pop(user_id, None)
                    user_data.pop(user_id, None)
                else:
                    send_message(chat_id, "📎 Зураг эсвэл файл хавсаргана уу.")
            return "ok"

        if normalized == "/form":
            user_states[user_id] = 0
            user_data[user_id] = {}
            send_message(chat_id, "📋 Гуйвуулгын форм эхэллээ:")
            send_message(chat_id, form_questions[0])
            return "ok"

        if normalized in ["/start", "меню", "эхлэх"]:
            keyboard = {
                "inline_keyboard": [
                    [{"text": "📋 Гуйвуулгын форм", "callback_data": "/form"}],
                    [{"text": "📈 Ханш", "callback_data": "ханш"}],
                    [{"text": "💸 Шимтгэл", "callback_data": "шимтгэл"}],
                    [{"text": "📄 Бичиг баримт", "callback_data": "баримт"}],
                    [{"text": "ℹ️ Бидний тухай", "callback_data": "тухай"}]
                ]
            }
            send_message(chat_id, "Та доорх цэснээс сонгоно уу:", reply_markup=keyboard)
            return "ok"

        if "ханш" in normalized:
            send_message(chat_id, "📈 Манай ханш: 1 юань = 462₮")
        elif "шимтгэл" in normalized:
            send_message(chat_id, "💰 Шимтгэлийн шатлал:
1¥-1,000¥ = 3,000₮ + 30¥
... → 100,000¥+ = 25,000₮ + 100¥")
        elif "утас" in normalized:
            send_message(chat_id, "📞 Утас: 80908090")
        elif "данс" in normalized:
            send_message(chat_id, "🏦 Данс:
Хаан: 5077407759
ХХБ: 431004884
Голомт: 3635112076
Төрийн банк: 343200497501
Хас: 5002742902")
        elif "баримт" in normalized or "бичиг" in normalized:
            send_message(chat_id, "📄 Шаардлагатай бичиг баримт:
- Илгээгчийн баримт
- Хүлээн авагчийн данс
- Гүйлгээний утга")
        elif "тухай" in normalized:
            send_message(chat_id, "📌 Бидний тухай:
7 дахь жилдээ юанийн шилжүүлэгт мэргэшин ажиллаж байна.
Технологид суурилсан, албан ёсны үйлчилгээ.")
        elif re.search(r"\d+", text):
            num = re.sub("[^\d]", "", text)
            if num:
                send_message(chat_id, calculate_fee(num))
        else:
            send_message(chat_id, "🤖 Та түлхүүр үг (ханш, шимтгэл...) эсвэл тоон дүн оруулна уу. /menu гэж бичиж болно.")

    elif callback:
        chat_id = callback["message"]["chat"]["id"]
        data = callback["data"]
        update = {"message": {"chat": {"id": chat_id}, "text": data, "from": callback["from"]}}
        request.json.update(update)
        return webhook()

    return "ok"

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
