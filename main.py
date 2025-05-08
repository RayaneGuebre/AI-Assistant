# ChaptGPT
from openai import OpenAI

import threading 
#Telegram
import telebot

#Environmental variables
import os
from os.path import join, dirname
from dotenv import load_dotenv

#Misc
import whisper
import requests

# Load Env variables

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_KEY")
TELEGRAM_ID = os.environ.get("TELEGRAM_ID")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
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



sent_with_telegram = False
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
    
        
    @bot.message_handler(func=lambda message: True)
    def to_gpt(message):
        output = chat_with_gpt(message.text)
        print(output)
        bot.reply_to(message, output)
 
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            break
        response = chat_with_gpt(user_input)
        print(f"Jarvis: {response}")
    
        

if __name__ == "__main__":
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    main()  
    
