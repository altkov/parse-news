class Recording:
    def __init__(self, db):
        self.db = db

    def save_news(self, news):
        duplicate_urls = [entry[0] for entry in self.get_duplicate_urls(
            [item['url'] for item in news]
        )]

        for item in news:
            if item['url'] in duplicate_urls:
                continue

            params = [item['title'], item['text'], item['img'], item['url'], 0]
            self.db.cursor().execute('INSERT INTO news (title, content, img, url, processed) VALUES (?, ?, ?, ?, ?)', params)

    def get_duplicate_urls(self, urls):
        cursor = self.db.cursor()
        query = 'SELECT url FROM news WHERE url IN ({})'.format(','.join('?'*len(urls)))
        cursor.execute(query, urls)
        return cursor.fetchall()
    
    def get_not_processed_news(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM news WHERE processed = 0')
        return cursor.fetchall()
    
    def process(self, id):
        cursor = self.db.cursor()
        cursor.execute('UPDATE news SET processed = 1 WHERE id = ?', [id])