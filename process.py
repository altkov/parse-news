import sqlite3
import telebot
from telebot.formatting import escape_markdown
from openai import OpenAI

from tools.recording import Recording

from config import ai_key
from config import tg_token

connection = sqlite3.connect('news.db')

ai = OpenAI(api_key=ai_key, base_url="https://api.aitunnel.ru/v1/")

recording = Recording(connection)
news = recording.get_not_processed_news()

bot = telebot.TeleBot(tg_token)
for item in news:
    id = item[0]
    title = item[1]
    text = item[2]
    img = item[3]

    if len(text) > 1024:
        prompt = "Сократи эту новость до " + str(950 - len(title)) + " знаков: \n "
        print(prompt)


        response = response = ai.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt + text},
            ],
            stream=False
        )

        text = response.choices[0].message.content

    message = '*'+escape_markdown(title)+'*\n\n'+escape_markdown(text)

    if len(message) < 4096:
        if img != '' and len(message) < 1025:
            bot.send_photo(1826968802, img, caption=message, parse_mode='MarkdownV2')
        else:
            bot.send_message(1826968802, message, parse_mode='MarkdownV2')

    recording.process(id)

connection.commit()
connection.close()