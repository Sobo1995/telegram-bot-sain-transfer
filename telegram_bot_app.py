
from flask import Flask, request
import telegram
import os
import re

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

HANSH = 462  # Static ханш

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

def normalize_input(text):
    replacements = {
        "ariljaa": "арилжаа", "hanh": "ханш", "hansh": "ханш",
        "belen": "бэлэн", "bus": "бус", "utas": "утас", "tugrug": "төгрөг",
        "yuani": "юань", "shimtghel": "шимтгэл", "shimtel": "шимтгэл",
        "bichig": "бичиг", "barimt": "баримт", "ashaardlaga": "шаардлага"
    }
    for latin, cyrillic in replacements.items():
        if latin in text:
            text += " " + cyrillic
    return text

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text.lower()
    message_text = normalize_input(message_text)

    response = ""

    if "бичиг баримт" in message_text or "шаардлагатай мэдээлэл" in message_text:
        response = (
            "📄 Шаардлагатай мэдээлэл, бичиг баримтын жагсаалт:\n"
            "- Илгээгчийн бичиг баримт (зураг, файл хэлбэрээр)\n"
            "- Хүлээн авагчийн бичиг баримт (зураг, файл хэлбэрээр)\n"
            "- Хүлээн авагчийн банкны нэр, дансны дугаар, банкны хаяг\n"
            "- Гүйлгээний дэлгэрэнгүй утга\n"
            "- Ажил үйлчилгээний гэрээ (*шаардлагатай тохиолдолд*)"
        )
    elif "арилжаа" in message_text:
        response = (
            "💱 Арилжаа хийх нөхцөл:\n"
            "Бид таны төлбөр тооцооны хэрэгцээнд юанийн бэлэн болон бэлэн бус арилжааг "
            "зах зээлд өрсөлдөхүйц уян хатан ханшаар тогтмол санал болгож байна.\n"
            "Та манай байнгын харилцагч болсноор илүү уян хатан ханш авах боломжтой.\n\n"
            "📌 Арилжаа хийхэд анхаарах зүйлс:\n"
            "- Өндөр дүнтэй арилжаа: Салбараар … сая төгрөг хүртэлх дүнтэй арилжааг шууд хийх боломжтой.\n"
            "- Бэлэн валют: бэлнээр байгаа эсвэл хадгаламжийн дансанд буй валют\n"
            "- Бэлэн бус валют: харилцах, карт, зээлийн данс, гадаад гуйвуулга гэх мэт"
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
        response = "Сайн байна уу! Та ханш, шимтгэл, арилжаа, бичиг баримт, эсвэл төгрөг/юанийн дүн оруулан асууж болно."

    bot.send_message(chat_id=chat_id, text=response)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
