
from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

def send_main_menu(chat_id):
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

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.effective_chat.id

    if update.message:
        send_main_menu(chat_id)
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
            response = (
                "ℹ️ Бидний тухай\n"
                "Бид хамгийн сүүлийн үеийн технологи, ухаалаг шийдлийг ашиглан харилцагчдын санхүүгийн хэрэглээг хялбаршуулах зорилгын дор 7 дахь жилдээ амжилттай үйл ажиллагаа явуулж байна.\n"
                "Дэлхийн стандартыг үйлчилгээндээ нэвтрүүлж, юанийн болон бусад гадаад төлбөр тооцоог цахимжуулан салбартаа түүчээлэгч нь болон ажиллаж байна.\n\n"
                "🎯 Үнэт зүйл: Ажилтан, Харилцагч, Нийгэм\n"
                "🔭 Алсын хараа: Оюунлаг ирээдүй, сайн сайхныг дэмжинэ\n"
                "🎯 Эрхэм зорилго: Юанийн шилжүүлгийн мэргэжлийн ёс зүйтэй, хууль ёсны дагуу гүйцэтгэн харилцагчийн санхүүгийн хэрэгцээг хялбаршуулна\n\n"
                "✅ ЭРСДЭЛГҮЙ: Хувийн мэдээлэл, мөнгөн хөрөнгийг хамгаалсан\n"
                "✅ АЛБАН ЁСНЫ: СЗХ-ны тусгай зөвшөөрөлтэй, хууль ёсны үйл ажиллагаа\n"
                "✅ ХУРДАН: Минутын дотор гүйлгээ хийх боломжтой\n"
                "✅ УЯН ХАТАН: Ханшийн уян хатан нөхцөлтэй"
            )

        bot.answer_callback_query(update.callback_query.id)
        bot.send_message(chat_id=chat_id, text=response)

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
