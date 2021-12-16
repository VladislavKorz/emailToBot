from loguru import logger
import time
from bd.commands import get_user_all
from email_work import emailCheck
from config import bot
from telebot import types

def start_mail():
    while True:
        try:
            time.sleep(1)
            list_user = get_user_all()
            if list_user:
                for user in list_user:
                    email_list = emailCheck(user[0], user[1], user[2]).get_email(True)
                    for item in email_list:
                        
                        markup = types.InlineKeyboardMarkup()
                        key1 = types.InlineKeyboardButton(text='Просмотреть', callback_data=f"email_view_{item.get('uid')}")
                        key2 = types.InlineKeyboardButton(text='Ответить', callback_data=f"email_otvet_{item.get('sender')}")
                        key3 = types.InlineKeyboardButton(text='Удалить', callback_data=f"email_delete_{item.get('uid')}")
                        markup.add(key1, key2,key3)
                        answ = f"{item.get('uid')} *От*: {item.get('sender')}\n*Тема*: {item.get('subject')}\n*Дата*: {item.get('date_send')}\n"
                        bot.send_message(user[3], answ, parse_mode='Markdown',reply_markup=markup)
        except:
            logger.error('Произошла ошибка, надо что-то исправить в проверке почты')
             