import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        article_text TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

conn.commit()
conn.close()