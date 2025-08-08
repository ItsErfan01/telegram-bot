import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

API_KEY = 'AIzaSyDL_EkgasRp9Olpd8frN3UvBefAbmYoYkY'
CX = 'd71d793b358914fde'
BOT_TOKEN = '8333975395:AAF5DL684XoAvRDmxauhh9KjddYq1FL75gI'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 سوالت رو بفرست تا برات جواب بدم.")

async def search_and_summarize(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': CX,
        'q': query,
        'num': 5,
        'hl': 'fa'
    }
    response = requests.get(url, params=params)
    data = response.json()

    snippets = [item.get("snippet") for item in data.get("items", []) if item.get("snippet")]
    if not snippets:
        return "❌ متأسفم، نتونستم اطلاعاتی پیدا کنم."

    # ترکیب خلاصه‌ها به یک پاسخ
    answer = "🧠 پاسخ به سوالت:\n\n" + "\n\n".join(snippets)
    return answer

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text("🔎 در حال بررسی و پاسخ‌گویی...")

    try:
        answer = await search_and_summarize(query)
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"⚠️ خطا:\n{e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    app.run_polling()

if __name__ == '__main__':
    main()