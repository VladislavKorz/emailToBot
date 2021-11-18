import datetime
import pandas
from loguru import logger
from bd.connector import conn


def log(username, status, text):
    cur = conn.cursor()
    now = str(datetime.datetime.now())
    msg = (now, username, status, text)
    cur.execute("INSERT INTO logger VALUES(NULL, ?, ?, ?, ?);", msg)
    conn.commit()
    cur.close()

def user_create(email, password, user_id, host='pop.gmail.com'):
    cur = conn.cursor()
    cur.execute(f"select * from users where email = '{email}'")
    if not cur.fetchall():
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?);", (email, password, host, user_id))
        conn.commit()
        msg = 'Create: Пользователь успешно создан!'
        log(email, 'SUCCESS', msg)
    else:
        msg = 'Error: Имя пользователя не уникально!'
        log(email, 'ERROR', msg)
    cur.close()
    return msg

