
from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.effective_chat.id

    if update.message and update.message.text == "/start":
        keyboard = [
            [InlineKeyboardButton("📤 Гуйвуулга", callback_data='guiwuulga'),
             InlineKeyboardButton("📈 Ханш", callback_data='hansh')],
            [InlineKeyboardButton("💰 Шимтгэл", callback_data='shimtgel'),
             InlineKeyboardButton("📄 Бичиг баримт", callback_data='barimt')],
            [InlineKeyboardButton("ℹ️ Бидний тухай", callback_data='bidnii_tuhai')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(
            chat_id=chat_id,
            text="Сайн байна уу! Та дараах үйлчилгээнээс сонгоно уу:",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        data = update.callback_query.data
        response = ""

        if data == "guiwuulga":
            response = "📤 Гуйвуулга хийхийн тулд таны бичиг баримт, хүлээн авагчийн мэдээлэл шаардлагатай. Та лавлах утсаар бидэнтэй холбогдоно уу: 80908090"
        elif data == "hansh":
            response = "📈 Манай ханш гүйлгээний нөхцлөөс хамааран уян хатан тогтоогддог. Та бидэнтэй холбогдон хамгийн таатай ханшийг аваарай!"
        elif data == "shimtgel":
            response = "💰 Шимтгэлийн шатлал:\n1 – 1,000¥ → 3,000₮ + 30¥\n1,000 – 10,000¥ → 5,000₮ + 50¥\n10,000 – 20,000¥ → 5,000₮ + 100¥\n20,000 – 50,000¥ → 10,000₮ + 100¥\n50,000 – 100,000¥ → 20,000₮ + 100¥\n100,000¥+ → 25,000₮ + 100¥"
        elif data == "barimt":
            response = "📄 Шаардлагатай бичиг баримт:\n- Илгээгчийн бичиг баримт (зураг, файл)\n- Хүлээн авагчийн бичиг баримт (зураг, файл)\n- Дансны мэдээлэл, банкны хаяг\n- Гүйлгээний утга\n- Ажил үйлчилгээний гэрээ (шаардлагатай тохиолдолд)"
        elif data == "bidnii_tuhai":
            response = "ℹ️ Бидний тухай:\n“Сайн Финанс ЭнП” нь сүүлийн үеийн технологи, ухаалаг шийдлүүдийг ашиглан гадаад төлбөр тооцоог хялбаршуулж, цахимжуулан үйлчилж буй байгууллага юм.\n📍 Найман шарга, Мөнгөт шарга төв #205\n🕘 Дав – Ба: 9:00 - 18:00, Онлайн гуйвуулга: 24/7\n📞 80908090"

        bot.answer_callback_query(update.callback_query.id)
        bot.send_message(chat_id=chat_id, text=response)

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
