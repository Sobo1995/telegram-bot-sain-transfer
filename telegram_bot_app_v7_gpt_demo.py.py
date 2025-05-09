
from flask import Flask, request
import telegram
import os
import re
import requests

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

GPT_API = "https://api.binjie.fun/api/gpt"  # Example public GPT proxy (unstable but free)
HANSH = 462

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
        "ariljaa": "арилжаа", "hansh": "ханш", "belen": "бэлэн", "bus": "бус",
        "tugrug": "төгрөг", "tug": "төгрөг", "t": "төгрөг", "yuan": "юань",
        "shimtgel": "шимтгэл", "bichig": "бичиг", "barimt": "баримт"
    }
    for latin, cyrillic in replacements.items():
        text = re.sub(rf"\b{latin}\b", cyrillic, text)
    text = re.sub(r"(\d{3,})\s*(tugrug|tug|t)", r"\1 төгрөг", text)
    text = re.sub(r"(\d{3,})\s*(yuan)", r"\1 юань", text)
    return text

def fallback_gpt_response(prompt):
    try:
        r = requests.post(GPT_API, json={"prompt": prompt})
        if r.ok:
            return r.json().get("text", "GPT-ээс хариу олдсонгүй.")
        else:
            return "GPT холболтын алдаа."
    except:
        return "GPT server-д холбогдож чадсангүй."

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text.lower()
    message_text = normalize_input(message_text)

    response = ""

    if "бичиг баримт" in message_text:
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
            "зах зээлд өрсөлдөхүйц уян хатан ханшаар тогтмол санал болгож байна."
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
                f"➡️ Шилжих дүн: {net:,}₮ → {final_yuan}¥"
            )
        elif yuan_match:
            yuan = int(yuan_match.group(1))
            fee_t, fee_y = get_fee_by_yuan(yuan)
            response = (
                f"💴 Таны оруулсан дүн: {yuan:,}¥\n"
                f"🧾 Шимтгэл: {fee_t:,}₮ + {fee_y}¥"
            )
        else:
            response = fallback_gpt_response(message_text)

    bot.send_message(chat_id=chat_id, text=response)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
