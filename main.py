from flask import Flask, request
import requests
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_KEY")

openai.api_key = OPENAI_KEY

# Flask route
@app.route("/", methods=["GET"])
def home():
    return "Jessy is live!"

@app.route("/", methods=["POST"])
def webhook():
    return "ok"  # Just respond OK, real logic runs through Telegram bot polling

# Telegram logic
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_message}],
    ).choices[0].message.content
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def run_bot():
    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app_telegram.run_polling()

# Start both Flask & Telegram
if __name__ == "__main__":
    from threading import Thread
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=5000)
