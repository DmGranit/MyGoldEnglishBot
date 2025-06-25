import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from gtts import gTTS
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hello! I am your English voice assistant.')

def handle_text(update, context):
    user_text = update.message.text
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        reply_text = response.choices[0].message.content
        update.message.reply_text(reply_text)
        tts = gTTS(reply_text)
        tts.save("response.mp3")
        with open("response.mp3", "rb") as audio:
            update.message.reply_voice(voice=audio)
    except Exception as e:
        logger.error("Error handling text: %s", e)
        update.message.reply_text("An error occurred. Please try again later.")

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
