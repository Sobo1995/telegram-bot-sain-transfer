import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

def send_message(chat_id, text):
    print(f"Sending message to {chat_id}: {text}")

chat_id = 123456789  # example ID, replace with actual logic

send_message(chat_id, "💡 Шимтгэл:\n1¥ - 1,000¥ = 3,000₮\n1,000¥ - 10,000¥ = 5,000₮\n10,000¥+ = 10,000-25,000₮")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
