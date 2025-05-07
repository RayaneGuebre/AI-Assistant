from openai import OpenAI

client = OpenAI()
import telegram
import os
from os.path import join, dirname
from dotenv import load_dotenv
import whisper
import requests

# Load Env variables

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
OPENAI_KEY = os.environ.get("OPENAI_KEY")
TELEGRAM_KEY = os.environ.get("TELEGRAM_BOT_KEY")
TELEGRAM_ID = os.environ.get("TELEGRAM_ID")
bot = telegram.Bot(token=TELEGRAM_KEY)

# test voice recognition 
#   model = whisper.load_model('base')
#    result = model.transcribe('test_audio.m4a', fp16=False)
#    print("ok we got here")
#    result['text']
#    print('finished')   

# GPT integration


sent_with_telegram = False
def chat_with_gpt(prompt):

    response =  client.chat.completions.create(
    model = "gpt-3.5-turbo",
    message= [{"role" : "user", "content" : prompt}])
    return response.choises[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower in ["bye", "exit", "quit"]:
            break
        response = chat_with_gpt(user_input)
        if sent_with_telegram:
            telegram.Chat.send_message(TELEGRAM_ID, response)