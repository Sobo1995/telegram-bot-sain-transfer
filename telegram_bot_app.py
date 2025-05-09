
from flask import Flask, request
import telegram
import os
import re

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

HANSH = 462  # Static for now

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

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text.lower()

    response = ""

    # Required documents info
    if "бичиг баримт" in message_text or "шаардлагатай мэдээлэл" in message_text:
        response = (
            "📄 Шаардлагатай мэдээлэл, бичиг баримтын жагсаалт:\n"
            "- Илгээгчийн бичиг баримт (зураг, файл хэлбэрээр)\n"
            "- Хүлээн авагчийн бичиг баримт (зураг, файл хэлбэрээр)\n"
            "- Хүлээн авагчийн банкны нэр, дансны дугаар, банкны хаяг\n"
            "- Гүйлгээний дэлгэрэнгүй утга\n"
            "- Ажил үйлчилгээний гэрээ (*шаардлагатай тохиолдолд*)"
        )
    else:
        # Check for amount input
        tugrug_match = re.search(r"(\d{3,})(\s*төгрөг|₮)", message_text)
        yuan_match = re.search(r"(\d{3,})(\s*юань|¥)", message_text)

        if tugrug_match:
            amount = int(tugrug_match.group(1))
            approx_yuan = amount / HANSH
            fee_t, fee_y = get_fee_by_yuan(approx_yuan)
            net = amount - fee_t
            final_yuan = round(net / HANSH, 2)
            response = (
                f"💰 Таны оруулсан дүн: {amount:,}₮\n"
                f"🧾 Шимтгэл: {fee_t:,}₮ + {fee_y}¥\n"
                f"💱 Ханш: 1 юань = {HANSH}₮\n"
                f"➡️ Шилжих дүн: {net:,}₮ → {final_yuan}¥"
            )
        elif yuan_match:
            yuan = int(yuan_match.group(1))
            fee_t, fee_y = get_fee_by_yuan(yuan)
            response = (
                f"💴 Таны оруулсан дүн: {yuan:,}¥\n"
                f"🧾 Шимтгэл: {fee_t:,}₮ + {fee_y}¥"
            )

    if not response:
        response = "Сайн байна уу! Та ханш, шимтгэл, бичиг баримтын шаардлага, эсвэл төгрөг/юанийн дүн оруулан шимтгэл бодох боломжтой."

    bot.send_message(chat_id=chat_id, text=response)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
