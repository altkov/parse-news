import html
import sqlite3
from tools.parser import Parser
from tools.recording import Recording

connection = sqlite3.connect('news.db')
parser = Parser()
feed = parser.parse_feed('https://rssexport.rbc.ru/rbcnews/news/10/full.rss')

news = []

for entry in feed.entries:
    text = entry['rbc_news_full-text']
    text = text.replace('Читайте РБК в Telegram.', '')
    text = text.replace('Обсудите новость в телеграм-канале «РБК Спорт».', '')

    while '\n\n' in text:
        text = text.replace('\n\n', '\n')

    item_to_append = {
        'title': html.unescape(entry['title']),
        'text': html.unescape(text),
        'url': entry['link']
    }

    img = entry.get('rbc_news_url')
    if img:
        item_to_append['img'] = img
    
    news.append(item_to_append)

recording = Recording(connection)
recording.save_news(news)

connection.commit()
connection.close()