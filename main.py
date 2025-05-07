import openai
import dotenv
import whisper
import requests
# test voice recognition 
#   model = whisper.load_model('base')
#    result = model.transcribe('test_audio.m4a', fp16=False)
#    print("ok we got here")
#    result['text']
#    print('finished')   

# GPT integration

def chat_with_gpt(prompt):
  
    response =  openai.chatCompletation.create(
        model = "gpt-3.5-turbo",
        message= [{"role" : "user", "content" : prompt}]
    )
    return response.choises[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower in ["bye", "exit", "quit"]:
            break
        response = chat_with_gpt(user_input)
        print(f"GPT: {response}")