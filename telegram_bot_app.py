
import os
import logging
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def send_message(chat_id, text, reply_markup=None):
    bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("📋 Гуйвуулгын форм", callback_data="form")],
        [InlineKeyboardButton("📈 Ханш", callback_data="rate")],
        [InlineKeyboardButton("💰 Шимтгэл", callback_data="fee")],
        [InlineKeyboardButton("📑 Бичиг баримт", callback_data="docs")],
        [InlineKeyboardButton("ℹ️ Бидний тухай", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Та доорх цэснээс сонгоно уу.", reply_markup=reply_markup)

def handle_message(update, context):
    text = update.message.text.lower()
    if any(key in text for key in ["ханш", "hansh"]):
        send_message(update.message.chat.id, "📈 Манай ханш: 1 юань = 462₮")
    elif any(key in text for key in ["шимтгэл", "shimtgel"]):
        send_message(update.message.chat.id, """💰 Шимтгэлийн шатлал:
1¥ - 1,000¥ = 3,000₮ + 30¥
1,000¥ - 10,000¥ = 5,000₮
10,000¥+ = 10,000-25,000₮""")
    elif any(key in text for key in ["бичиг баримт", "barimt", "bichig", "barimt"]):
        send_message(update.message.chat.id, "📑 Бүрдүүлэх бичиг баримт:
Илгээгч, хүлээн авагчийн бичиг баримт
Дансны дугаар, банкны нэр
Гүйлгээний утга")
    elif any(key in text for key in ["тухай", "company", "about", "bid"]):
        send_message(update.message.chat.id, "ℹ️ Бидний тухай:
Сайн Трансфер нь 7 жилийн турш харилцагчдын санхүүгийн хэрэгцээг хялбаршуулах зорилготой ажиллаж байна.")
    elif any(key in text for key in ["утас", "dugaar", "utas", "holboo"]):
        send_message(update.message.chat.id, "📞 Холбоо барих: 80908090")
    else:
        start(update, context)

def handle_callback(update, context):
    query = update.callback_query
    data = query.data
    if data == "rate":
        send_message(query.message.chat_id, "📈 Манай ханш: 1 юань = 462₮")
    elif data == "fee":
        send_message(query.message.chat_id, "💰 Шимтгэлийн шатлал:
1¥ - 1,000¥ = 3,000₮ + 30¥
1,000¥ - 10,000¥ = 5,000₮
10,000¥+ = 10,000-25,000₮")
    elif data == "docs":
        send_message(query.message.chat_id, """📑 Бүрдүүлэх бичиг баримт:
Илгээгч, хүлээн авагчийн бичиг баримт
Дансны дугаар, банкны нэр
Гүйлгээний утга""")
    elif data == "about":
        send_message(query.message.chat_id, "ℹ️ Бидний тухай:
Сайн Трансфер нь 7 жилийн турш харилцагчдын санхүүгийн хэрэгцээг хялбаршуулах зорилготой ажиллаж байна.")
    elif data == "form":
        send_message(query.message.chat_id, "📋 Гуйвуулгын форм бөглөх хэсэг (шинэчлэгдэж байна)...")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Telegram bot is running"

dp = Dispatcher(bot, None, workers=0, use_context=True)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
dp.add_handler(MessageHandler(Filters.command, handle_message))
dp.add_handler(MessageHandler(Filters.all, handle_message))
dp.add_handler(MessageHandler(Filters.callback_query, handle_callback))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
