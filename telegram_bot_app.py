
from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import re

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
HANSH = 462

user_states = {}
user_data = {}
questions = [
    "1. Хүлээн авагчийн нэр?",
    "2. Банкны нэр?",
    "3. Дансны дугаар?",
    "4. Илгээгчийн нэр?",
    "5. Утасны дугаар?",
    "6. Гүйлгээний утга?",
    "7. Иргэний үнэмлэх, бичиг баримт зураг илгээнэ үү"
]

def send_main_menu(chat_id):
    keyboard = [
        [InlineKeyboardButton("📤 Гуйвуулга", callback_data='гуйвуулга'),
         InlineKeyboardButton("📈 Ханш", callback_data='ханш')],
        [InlineKeyboardButton("💰 Шимтгэл", callback_data='шимтгэл'),
         InlineKeyboardButton("📄 Бичиг баримт", callback_data='баримт')],
        [InlineKeyboardButton("ℹ️ Бидний тухай", callback_data='бидний тухай'), InlineKeyboardButton("📋 Гуйвуулгын форм", callback_data='/form')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=chat_id,
        text="Сайн байна уу! Та дараах үйлчилгээнээс сонгоно уу:",
        reply_markup=reply_markup
    )

def normalize_input(text):
    text = text.lower()
    latin_map = {
        "hansh": "ханш", "shimtgel": "шимтгэл", "barimt": "баримт", "bichig": "бичиг",
        "tuhai": "тухай", "bidnii": "бидний", "guiwuulga": "гуйвуулга", "guivuulga": "гуйвуулга",
        "dans": "данс", "dugaar": "дугаар", "utas": "утас", "holbogdoh": "холбогдох",
        "tugrug": "төгрөг", "tug": "төгрөг", "yuan": "юань", "form": "/form"
    }
    for latin, cyrillic in latin_map.items():
        text = re.sub(rf"\b{latin}\b", cyrillic, text)
    text = re.sub(r"(\d{3,})\s*(tug|₮|төгрөг)", r"\1 төгрөг", text)
    text = re.sub(r"(\d{3,})\s*(yuan|юань|¥)", r"\1 юань", text)
    return text

def get_fee_by_yuan(yuan):
    if yuan <= 1000:
        return 3000, 30
    elif yuan <= 10000:
        return 5000, 50
    elif yuan <= 20000:
        return 5000, 100
    elif yuan <= 50000:
        return 10000, 100
    elif yuan <= 100000:
        return 20000, 100
    else:
        return 25000, 100

def handle_keyword(chat_id, text):
    text = normalize_input(text)
    if "гуйвуул" in text:
        return "📤 Гуйвуулга хийхийн тулд таны бичиг баримт, хүлээн авагчийн мэдээлэл шаардлагатай. Та лавлах утсаар бидэнтэй холбогдоно уу: 80908090"
    elif "ханш" in text:
        return "📈 Манай ханш гүйлгээний нөхцлөөс хамааран уян хатан тогтоогддог. Та бидэнтэй холбогдон хамгийн таатай ханшийг аваарай!"
    elif "шимтгэл" in text:
        return "💰 Шимтгэлийн шатлал:\n1 – 1,000¥ → 3,000₮ + 30¥\n1,000 – 10,000¥ → 5,000₮ + 50¥\n10,000 – 20,000¥ → 5,000₮ + 100¥\n20,000 – 50,000¥ → 10,000₮ + 100¥\n50,000 – 100,000¥ → 20,000₮ + 100¥\n100,000¥+ → 25,000₮ + 100¥"
    elif "баримт" in text or "бичиг" in text:
        return "📄 Шаардлагатай бичиг баримт:\n- Илгээгчийн бичиг баримт (зураг, файл)\n- Хүлээн авагчийн бичиг баримт (зураг, файл)\n- Дансны мэдээлэл, банкны хаяг\n- Гүйлгээний утга\n- Ажил үйлчилгээний гэрээ (шаардлагатай тохиолдолд)"
    elif "бидний тухай" in text or "тухай" in text:
        return (
            "ℹ️ Бидний тухай\n"
            "Бид хамгийн сүүлийн үеийн технологи, ухаалаг шийдлийг ашиглан харилцагчдын санхүүгийн хэрэглээг хялбаршуулах зорилгын дор 7 дахь жилдээ амжилттай үйл ажиллагаа явуулж байна.\n"
            "✅ ЭРСДЭЛГҮЙ\n✅ АЛБАН ЁСНЫ\n✅ ХУРДАН\n✅ УЯН ХАТАН"
        )
    elif "данс" in text or "дугаар" in text:
        return (
            "🏦 Дансны дугаарууд:\n"
            "- Хаан банк: 5077407759\n"
            "- Худалдаа Хөгжлийн Банк: 431004884\n"
            "- Голомт: 3635112076\n"
            "- Төрийн Банк: 343200497501\n"
            "- Хас Банк: 5002742902"
        )
    elif "утас" in text or "холбогдох" in text:
        return "📞 Манай холбогдох утас: 80908090"

    tugrug_match = re.search(r"(\d{3,})\s*төгрөг", text)
    yuan_match = re.search(r"(\d{3,})\s*юань", text)
    if tugrug_match:
        amount = int(tugrug_match.group(1))
        approx_yuan = amount / HANSH
        fee_t, fee_y = get_fee_by_yuan(approx_yuan)
        net = amount - fee_t
        final_yuan = round(net / HANSH, 2)
        return f"💰 {amount:,}₮ → Шимтгэл: {fee_t:,}₮ + {fee_y}¥ → {final_yuan}¥"
    elif yuan_match:
        yuan = int(yuan_match.group(1))
        fee_t, fee_y = get_fee_by_yuan(yuan)
        return f"💴 {yuan:,}¥ → Шимтгэл: {fee_t:,}₮ + {fee_y}¥"

    return None


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        message = update.message
        chat_id = message.chat.id
        user_id = message.from_user.id

        if message.text and message.text.lower().strip() == "/form":
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
                    user_states.pop(user_id)
                else:
                    bot.send_message(chat_id=chat_id, text="📎 Зураг буюу файл илгээнэ үү.")
            return "ok"

        if message.text:
            reply = handle_keyword(chat_id, message.text)
            if reply:
                bot.send_message(chat_id=chat_id, text=reply)
            else:
                send_main_menu(chat_id)

    elif update.callback_query:
        data = update.callback_query.data
        chat_id = update.callback_query.message.chat.id
        user_id = update.callback_query.from_user.id

        if data == "/form":
            user_states[user_id] = 0
            user_data[user_id] = {}
            bot.answer_callback_query(update.callback_query.id)
            bot.send_message(chat_id=chat_id, text="📋 Гуйвуулгын форм бөглөж эхэлцгээе.")
            bot.send_message(chat_id=chat_id, text=questions[0])
            return "ok"

        reply = handle_keyword(chat_id, data)
        bot.answer_callback_query(update.callback_query.id)
        bot.send_message(chat_id=chat_id, text=reply)

    return "ok"
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
                user_states.pop(user_id)
            else:
                bot.send_message(chat_id=chat_id, text="📎 Зураг буюу файл илгээнэ үү.")
        return "ok"

    if message.text:
        reply = handle_keyword(chat_id, message.text)
        if reply:
            bot.send_message(chat_id=chat_id, text=reply)
        else:
            send_main_menu(chat_id)

    elif update.callback_query:
        data = update.callback_query.data
        chat_id = update.callback_query.message.chat.id
        user_id = update.callback_query.from_user.id

        if data == "/form":
            user_states[user_id] = 0
            user_data[user_id] = {}
            bot.answer_callback_query(update.callback_query.id)
            bot.send_message(chat_id=chat_id, text="📋 Гуйвуулгын форм бөглөж эхэлцгээе.")
            bot.send_message(chat_id=chat_id, text=questions[0])
            return "ok"

        reply = handle_keyword(chat_id, data)
        bot.answer_callback_query(update.callback_query.id)
        bot.send_message(chat_id=chat_id, text=reply)

        bot.answer_callback_query(update.callback_query.id)
        bot.send_message(chat_id=chat_id, text=reply)

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
