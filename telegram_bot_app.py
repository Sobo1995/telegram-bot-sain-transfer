
# v21 - Telegram bot form flow (structure only)
# Note: This is a placeholder code. The full implementation will track states.

from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

user_states = {}  # user_id: step
user_data = {}    # user_id: {answers}

questions = [
    "1. Хүлээн авагчийн нэр?",
    "2. Банкны нэр?",
    "3. Дансны дугаар?",
    "4. Илгээгчийн нэр?",
    "5. Утасны дугаар?",
    "6. Гүйлгээний утга?",
    "7. Иргэний үнэмлэх, бичиг баримт зураг илгээнэ үү"
]

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message = update.message
    chat_id = message.chat.id
    user_id = message.from_user.id

    if message.text and message.text.lower() == "/form":
        user_states[user_id] = 0
        user_data[user_id] = {}
        bot.send_message(chat_id=chat_id, text="📋 Гуйвуулгын форм бөглөж эхэлцгээе.")
        bot.send_message(chat_id=chat_id, text=questions[0])
        return "ok"

    if user_id in user_states:
        step = user_states[user_id]
        if step < len(questions) - 1:
            user_data[user_id][f"q{step+1}"] = message.text
            user_states[user_id] += 1
            bot.send_message(chat_id=chat_id, text=questions[step+1])
        else:
            if message.document or message.photo:
                user_data[user_id]["q7_file"] = "Файл хүлээн авсан"
                bot.send_message(chat_id=chat_id, text="✅ Бүх мэдээлэл амжилттай бүртгэгдлээ. Баярлалаа.")
            else:
                bot.send_message(chat_id=chat_id, text="📎 Зураг буюу файл илгээнэ үү.")
    else:
        bot.send_message(chat_id=chat_id, text="Та /form гэж бичиж гуйвуулгын форм бөглөнө үү.")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
