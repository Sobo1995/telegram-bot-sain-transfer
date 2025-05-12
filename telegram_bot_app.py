
from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import re

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
HANSH = 462

def send_main_menu(chat_id):
    keyboard = [
        [InlineKeyboardButton("📤 Гуйвуулга", callback_data='guiwuulga'),
         InlineKeyboardButton("📈 Ханш", callback_data='hansh')],
        [InlineKeyboardButton("💰 Шимтгэл", callback_data='shimtgel'),
         InlineKeyboardButton("📄 Бичиг баримт", callback_data='barimt')],
        [InlineKeyboardButton("ℹ️ Бидний тухай", callback_data='bidnii_tuhai')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id,
                     text="Сайн байна уу! Та дараах үйлчилгээнээс сонгоно уу:",
                     reply_markup=reply_markup)

def normalize_input(text):
    text = text.lower()
    latin_map = {
        "hansh": "ханш", "shimtgel": "шимтгэл", "barimt": "баримт", "bichig": "бичиг",
        "tuhai": "тухай", "bidnii": "бидний", "guiwuulga": "гуйвуулга", "guivuulga": "гуйвуулга",
        "dans": "данс", "dugaar": "дугаар", "utas": "утас", "holbogdoh": "холбогдох",
        "tugrug": "төгрөг", "tug": "төгрөг", "yuan": "юань"
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
            "Дэлхийн стандартыг үйлчилгээндээ нэвтрүүлж, юанийн болон бусад гадаад төлбөр тооцоог цахимжуулан салбартаа түүчээлэгч нь болон ажиллаж байна.\n\n"
            "🎯 Үнэт зүйл: Ажилтан, Харилцагч, Нийгэм\n"
            "🔭 Алсын хараа: Оюунлаг ирээдүй, сайн сайхныг дэмжинэ\n"
            "🎯 Эрхэм зорилго: Юанийн шилжүүлгийн мэргэжлийн ёс зүйтэй, хууль ёсны дагуу гүйцэтгэн харилцагчийн санхүүгийн хэрэгцээг хялбаршуулна\n\n"
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
    chat_id = update.effective_chat.id

    if update.message and update.message.text:
        reply = handle_keyword(chat_id, update.message.text)
        if reply:
            bot.send_message(chat_id=chat_id, text=reply)
        else:
            send_main_menu(chat_id)

    elif update.callback_query:
        data = update.callback_query.data
        response = handle_keyword(chat_id, data)
        bot.answer_callback_query(update.callback_query.id)
        bot.send_message(chat_id=chat_id, text=response)

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
