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

#Calendar
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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



SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())


service = build("calendar", "v3", credentials=creds)







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
        if str(message.from_user.id) != TELEGRAM_ID:
            print(f"Ignored message from unauthorized user: {message.from_user.id}")
            return
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
    
