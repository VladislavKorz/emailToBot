import sqlite3

with sqlite3.connect("user.db", check_same_thread=False) as conn:
    cur = conn.cursor()
    
    cur.executescript("""CREATE TABLE IF NOT EXISTS logger(
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time DATETIME,
        user TEXT,
        status TEXT,
        text TEXT);
    """)
    
    cur.executescript("""CREATE TABLE IF NOT EXISTS users(
        email VARCHAR (255) NOT NULL PRIMARY KEY,
        password VARCHAR (255) NOT NULL,
        host VARCHAR (20) DEFAULT 'pop.gmail.com',
        user_id INTEGER (15));
    """)
    
    conn.commit()
