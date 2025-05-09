
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
        "tug": "төгрөг", "t": "төгрөг", "yuan": "юань", "yuani": "юань",
        "shimtghel": "шимтгэл", "shimtgel": "шимтгэл", "bichig": "бичиг", "barimt": "баримт"
    }
    for latin, cyrillic in replacements.items():
        text = re.sub(rf"\b{latin}\b", cyrillic, text)
    # also support cases like "100000tugrug"
    text = re.sub(r"(\d{3,})\s*(tugrug|tug|t)", r"\1 төгрөг", text)
    text = re.sub(r"(\d{3,})\s*(yuan|yuani)", r"\1 юань", text)
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
    elif "ханш" in message_text:
        response = f"📈 Манай ханш: 1 юань = {HANSH}₮"
    elif "шимтгэл" in message_text:
        response = (
            "🧾 Шимтгэлийн шатлал:\n"
            "1 – 1,000¥ → 3,000₮ + 30¥\n"
            "1,000 – 10,000¥ → 5,000₮ + 50¥\n"
            "10,000 – 20,000¥ → 5,000₮ + 100¥\n"
            "20,000 – 50,000¥ → 10,000₮ + 100¥\n"
            "50,000 – 100,000¥ → 20,000₮ + 100¥\n"
            "100,000¥+ → 25,000₮ + 100¥"
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
