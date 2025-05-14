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
import json

#Calendar

from datetime import date, time, datetime
import time
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


date_string = f"Today's date is: {date.today()} and time: {datetime.now()}"
initial_prompt = '''
You are my personal AI assistant. I'm Rayan, a 15-year-old student and engineering enthusiast. 
I like to build things using Python, 3D printing, and electronics.
You should help me with my projects, manage my schedule, and explain things clearly when I ask questions.
You can access my Google Calendar and Telegram messages.

to work with third party app you need to use commands

to separate the command from the message add "===commands===" at the end of the message.





Keep answers short and focused unless I ask for more details.




If i specificaly ask you to add an event to my calendar add the following  line after your message: "===" and under it "add_event", and then fill this witht the infos: 
  {
  'summary': '', if not specified generate it
  'location': '', if not specified generate it
  'description': '',
  'start': {
    'dateTime': '', in the format '2015-05-28T09:00:00-07:00'
    'timeZone': 'Europe/Bruxelles',
  },
  'end': {
    'dateTime': '', in the format 2015-05-28T09:00:00-07:00, if not specified make it last one hour,
    'timeZone': 'Europe/Bruxelles'
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

if i didn't ask you don't add it
if i didn't specified the time add it to the memory, and add it later when i'll have specified the time
remember first "===commands===" and then the command

to add something to the memory use the command "add_memory"

remeber that your message structure needs to be like:

"your message"
===commands===
add_event
the json 
===
add_memory
what you need to remember
===
and then write what you should remember
Here's the message i just sent you:

'''
initial_prompt += date_string




def chat_with_gpt(prompt):

    headers = {
    'Content-Type': 'application/json',
    }

    json_data = {
    'messages': [
        {
            'role': 'user',
            'content': initial_prompt + prompt,
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
        if "===commands===" in output:
            finished_output = output.split("===commands===")[0]
            commands = output.split("===commands===")[1]
            commands = commands.split("===")
            for command in commands:
                if "add_event" in command:
                    command = command.replace("add_event", "")
                    print(command)
                    command = json.dumps(command)
                    event = service.events().insert(calendarId='95746b9ff028195c12a3754a5b52ccc3ed800951daf60f999413096bcff5aeb7@group.calendar.google.com', body=command).execute()
                    print("event added succesfully")
                if "add_memory" in command:
                    command.replace("add_memory", "")
                    
                    with open(memory.txt, "a") as memory:
                        memory.write(command)
                


        print(output)
        bot.reply_to(message, finished_output)
        
 
    
    while True:

        
     
     

        

        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            break
        output = chat_with_gpt(user_input)
        
        if "===commands===" in output:
            finished_output = output.split("===add_event===")[0]
            commands = output.split("===add_event===")[1]
            commands = commands.split("===")
            for command in commands:
                if "add_event" in command:
                    command.replace("add_event", "")
                    event = service.events().insert(calendarId='95746b9ff028195c12a3754a5b52ccc3ed800951daf60f999413096bcff5aeb7@group.calendar.google.com', body=json.loads(command)).execute()
                    print("event added succesfully")
                if "add_memory" in command:
                    command.replace("add_memory", "")
                    
                    with open(memory.txt, "a") as memory:
                        memory.write(command)
        else:
            response = output
        print(date.today())
        print(f"Jarvis: {response}")
   
        

if __name__ == "__main__":
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    main()  

    
