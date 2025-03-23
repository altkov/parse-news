import httpx
import feedparser

class Parser:
    def parse_feed(self, url):
        response = httpx.get(url)
        return feedparser.parse(response)