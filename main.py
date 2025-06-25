import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import openai
from gtts import gTTS
from io import BytesIO

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
updater = Updater(TELEGRAM_TOKEN)

def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a friendly English tutor."},
            {"role": "user", "content": user_text}
        ]
    )

    bot_reply = response.choices[0].message.content
    tts = gTTS(bot_reply, lang='en')
    voice_fp = BytesIO()
    tts.write_to_fp(voice_fp)
    voice_fp.seek(0)

    update.message.reply_voice(voice=voice_fp, caption=bot_reply)

updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
updater.start_polling()
updater.idle()
