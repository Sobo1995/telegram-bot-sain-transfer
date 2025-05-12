
from flask import Flask, request
import telegram
import os
import re
import requests

TOKEN = "7913606596:AAFnw_ur4a5U0hs2mbeD-kAeZwIXJY89-pI"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

HANSH = 462
OPENROUTER_API_KEY = "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"
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
GPT_MODEL = "mistralai/mistral-7b-instruct"

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

def ask_openrouter(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GPT_MODEL,
            "messages": [
                {"role": "system", "content": "Та бол Сайн Финанс компанийн туслах AI чатбот. Та зөвхөн кирилл үсгээр хариулна. Танай компанийн үйлчилгээ, ханш, шимтгэл, бичиг баримтын шаардлага зэрэг мэдээлэлд энгийнээр тайлбар өг."},
                {"role": "user", "content": prompt}
            ]
        }
        r = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=payload)
        if r.ok:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return "GPT серверээс хариу авч чадсангүй."
    except Exception:
        return "GPT серверт холбогдох үед алдаа гарлаа."

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text.lower()
    message_text = normalize_input(message_text)

    response_parts = []

    if "бичиг баримт" in message_text:
        response_parts.append(
            "📄 Шаардлагатай мэдээлэл, бичиг баримтын жагсаалт:\n"
            "- Илгээгчийн бичиг баримт (зураг, файл хэлбэрээр)\n"
            "- Хүлээн авагчийн бичиг баримт (зураг, файл хэлбэрээр)\n"
            "- Хүлээн авагчийн банкны нэр, дансны дугаар, банкны хаяг\n"
            "- Гүйлгээний дэлгэрэнгүй утга\n"
            "- Ажил үйлчилгээний гэрээ (*шаардлагатай тохиолдолд*)"
        )
    if "арилжаа" in message_text:
        response_parts.append(
            "💱 Арилжаа хийх нөхцөл:\n"
            "Бид таны төлбөр тооцооны хэрэгцээнд юанийн бэлэн болон бэлэн бус арилжааг "
            "зах зээлд өрсөлдөхүйц уян хатан ханшаар тогтмол санал болгож байна."
        )
    if "ханш" in message_text:
        response_parts.append(f"📈 Манай ханш: 1 юань = {HANSH}₮")
    if "шимтгэл" in message_text:
        response_parts.append(
            "🧾 Шимтгэлийн шатлал:\n"
            "1 – 1,000¥ → 3,000₮ + 30¥\n"
            "1,000 – 10,000¥ → 5,000₮ + 50¥\n"
            "10,000 – 20,000¥ → 5,000₮ + 100¥\n"
            "20,000 – 50,000¥ → 10,000₮ + 100¥\n"
            "50,000 – 100,000¥ → 20,000₮ + 100¥\n"
            "100,000¥+ → 25,000₮ + 100¥"
        )

    tugrug_match = re.search(r"(\d{3,})(\s*төгрөг|₮)", message_text)
    yuan_match = re.search(r"(\d{3,})(\s*юань|¥)", message_text)

    if tugrug_match:
        amount = int(tugrug_match.group(1))
        approx_yuan = amount / HANSH
        fee_t, fee_y = get_fee_by_yuan(approx_yuan)
        net = amount - fee_t
        final_yuan = round(net / HANSH, 2)
        response_parts.append(
            f"💰 Таны оруулсан дүн: {amount:,}₮\n"
            f"🧾 Шимтгэл: {fee_t:,}₮ + {fee_y}¥\n"
            f"➡️ Шилжих дүн: {net:,}₮ → {final_yuan}¥"
        )
    elif yuan_match:
        yuan = int(yuan_match.group(1))
        fee_t, fee_y = get_fee_by_yuan(yuan)
        response_parts.append(
            f"💴 Таны оруулсан дүн: {yuan:,}¥\n"
            f"🧾 Шимтгэл: {fee_t:,}₮ + {fee_y}¥"
        )

    # Always add GPT fallback at the end
    ai_answer = ask_openrouter(message_text)
    response_parts.append("🧠 GPT AI:\n" + ai_answer)

    final_response = "\n\n".join(response_parts)
    bot.send_message(chat_id=chat_id, text=final_response)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
