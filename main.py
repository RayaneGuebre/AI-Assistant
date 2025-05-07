from openai import OpenAI

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

import os
from os.path import join, dirname
from dotenv import load_dotenv
import whisper
import requests

# Load Env variables

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_KEY = os.environ.get("TELEGRAM_BOT_KEY")
TELEGRAM_ID = os.environ.get("TELEGRAM_ID")
bot = telegram.Bot(token=TELEGRAM_KEY)
client = OpenAI(
    api_key = OPENAI_API_KEY,
)
# test voice recognition 
#   model = whisper.load_model('base')
#    result = model.transcribe('test_audio.m4a', fp16=False)
#    print("ok we got here")
#    result['text']
#    print('finished')   

# GPT integration


sent_with_telegram = True
def chat_with_gpt(prompt):

    headers = {
    'Content-Type': 'application/json',
    }

    json_data = {
    'messages': [
        {
            'role': 'user',
            'content': prompt,
        },
    ],
}
    response = requests.post('https://ai.hackclub.com/chat/completions', headers=headers, json=json_data)
    data = response.json()
    return data["choices"][0]["message"]["content"]
def main():
    application = ApplicationBuilder().token(TELEGRAM_KEY).build()
    
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello! I'm your assistant.")
        
    while True:
        user_input = input("You: ")
            
        if user_input.lower() in ["bye", "exit", "quit"]:
            break
        response = chat_with_gpt(user_input)
        if sent_with_telegram:
            telegram.Chat.send_message(TELEGRAM_ID, response)
        else: 
                print(f"Jarvis: {response}")

if __name__ == "__main__":
    main()  