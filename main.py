import os
import tempfile
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gtts import gTTS
import openai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 Hi! Send me any English message and I will reply with a voice response.")

def handle_text(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    # Отправка текста в OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly English-speaking assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response['choices'][0]['message']['content']

    # Преобразуем ответ в речь
    tts = gTTS(text=reply, lang='en')
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tf:
        tts.save(tf.name)
        with open(tf.name, 'rb') as audio:
            update.message.reply_voice(audio)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
