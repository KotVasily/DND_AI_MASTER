import openai
import config
import time

client = openai.OpenAI(api_key=config.api_key, base_url="https://api.naga.ac/v1")

def get_text(text, message_list:list, client: openai.OpenAI, save_message=True):
    message_list.append({
         "role": "user",
        "content": text
    })
    chat_completion = client.chat.completions.create(
        messages=message_list,
        model="gpt-4o-mini"
    )

    if not save_message:
        message_list.pop(-1)
    return chat_completion.choices[0].message.content

def get_image(text, client: openai.OpenAI):
    response = client.images.generate(
          model="kandinsky-3.1",
          prompt=text,
          size="1024x1024",
          quality="standard",
          n=1)
    
    return response.data[0].url