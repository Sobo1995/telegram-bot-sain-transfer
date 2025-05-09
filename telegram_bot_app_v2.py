
from flask import Flask, request
import telegram
import os

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text.lower()

    # Response logic
    if "ханш" in message_text:
        response = "2025 оны 5-р сарын 9-ны байдлаар 1 юань = 462₮ байна."
    elif "агент" in message_text or "хаана" in message_text:
        response = "Манайх онлайн захиалга авч, түргэн шуурхай найдвартай шилжүүлдэг."
    elif "шимтгэл" in message_text or "хураамж" in message_text:
        response = "Шимтгэл 100,000₮-с доош бол 3,000₮, 100,000₮-с дээш бол 5,000₮ байна."
    elif "та нарын тухай" in message_text or "юу хийдэг вэ" in message_text or "сайн финанс" in message_text:
        response = "Бид хамгийн сүүлийн үеийн технологи, ухаалаг шийдлийг ашиглан харилцагчдын санхүүгийн хэрэглээг хялбаршуулах зорилгын дор 7 дахь жилдээ амжилттай үйл ажиллагаа явуулж байна. Дэлхийн стандартыг үйлчилгээндээ нэвтрүүлж, юанийн болон бусад гадаад төлбөр тооцоог цахимжуулан салбартаа түүчээлэгч нь болон ажиллаж байна."
    elif "цагийн хуваарь" in message_text or "ажлын цаг" in message_text:
        response = "Дав – Ба: 9:00 - 18:00\nОнлайн гуйвуулга: 24/7"
    elif "утас" in message_text or "дугаар" in message_text or "холбогдох" in message_text:
        response = "Та бидэнтэй 80908090 дугаараар холбогдоорой."
    elif "байршил" in message_text or "оффис" in message_text or "хаана" in message_text:
        response = "Бид Найман шаргын “Мөнгөт Шарга төв”-ийн 205 тоотод байрлаж байна."
    elif "вэб" in message_text or "сайт" in message_text or "хуудас" in message_text:
        response = "Манай вэбсайт: https://www.sainbbsb.mn"
    else:
        response = "Сайн байна уу! Та ханш, шимтгэл, агент, цагийн хуваарь, байршлын талаар асууж болно."

    bot.send_message(chat_id=chat_id, text=response)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
