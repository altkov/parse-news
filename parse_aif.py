import httpx
import sqlite3
from strip_tags import strip_tags
from bs4 import BeautifulSoup

from tools.parser import Parser
from tools.recording import Recording

connection = sqlite3.connect('news.db')
parser = Parser()
feed = parser.parse_feed('https://aif.ru/rss/news.php')

news = []

for entry in feed.entries[0:9]:
    item_url = entry.link
    title = entry.title
    img = ''

    response = httpx.get(item_url)

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find('div', {'class': 'article_text'}).get_text().strip()
    img = soup.select('.content_body .img_box img')[0].attrs['src']

    print(img)

    while '\n\n' in text:
        text = text.replace('\n\n', '\n')

    news.append({
        'title': title,
        'text': text,
        'img': img,
        'url': item_url
    })

recording = Recording(connection)
recording.save_news(news)

connection.commit()
connection.close()