
from flask import Flask, request
import telegram

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    text = message_text.lower()
    if "ханш" in text:
        response = "2025 оны 5-р сарын 9-ны байдлаар 1 юань = 462₮ байна."
    elif "агент" in text or "хаана" in text:
        response = "Манайх онлайн захиалга авч, түргэн шуурхай найдвартай шилжүүлдэг."
    elif "шимтгэл" in text or "хураамж" in text:
        response = "Шимтгэл 100,000₮-с доош бол 3,000₮, 100,000₮-с дээш бол 5,000₮ байна."
    else:
        response = "Сайн байна уу! Та ханш, шимтгэл эсвэл агентын талаар асууж болно."

    bot.send_message(chat_id=chat_id, text=response)
    return "ok"
