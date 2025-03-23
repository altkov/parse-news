DROP TABLE IF EXISTS news;
CREATE TABLE news (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    img VARCHAR(255),
    url VARCHAR(255),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    processed INTEGER
);