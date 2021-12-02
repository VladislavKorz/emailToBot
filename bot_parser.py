from logging import log
from telebot import types
import email
import imaplib
from time import sleep
from loguru import logger
from email_test import emailCheck
from config import bot
from bot_login import *
from bd.commands import *

logger.info(f"Бот запущен")


@bot.message_handler(commands=['start'])
def bot_command_start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg'))
    markup.add(types.InlineKeyboardButton(text='Подробнее про бота', callback_data='more'))
    markup.add(types.InlineKeyboardButton(text='Сказать идею', callback_data='say'))
    bot.send_message(message.chat.id, text="Здравствуйте {0.first_name},для дальнейшей работы выберите нужную кнопку.".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['help'])
def bot_command_help(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='На главную', callback_data='owner'))
    bot.send_message(message.chat.id,text='Выберите пункт',reply_markup=markup)


@bot.message_handler(commands=['settings'])
def bot_command_settings(message):
    bot.send_message(message.chat.id,'Скоро тут будут настройки!')


@bot.message_handler(commands=['home'])
def bot_command_settings(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Показать полностью', callback_data='view_all'))
    markup.add(types.InlineKeyboardButton(text='Отметить прочитанным', callback_data='mark_read'))
    markup.add(types.InlineKeyboardButton(text='Ответить', callback_data='answer'))
    markup.add(types.InlineKeyboardButton(text='Удалить', callback_data='delete'))
    bot.send_message(message.chat.id,text='Выберите нужный пункт',reply_markup=markup)

@bot.message_handler(commands=['email'])
def bot_command_email(message):
    user = user_login(message.from_user.id)
    if user:
        logger.info(user)
        email_list = emailCheck(user[0], user[1], user[2]).get_email()
        if len(email_list) > 4:
            email_list = email_list[:4]
        for item in email_list:
            answ = f"*От*: {item.get('sender')}\n*Тема*: {item.get('subject')}\n*Дата*: {item.get('date_send')}\n*Статус*: {item.get('type')}\n"
            bot.send_message(message.chat.id, answ, parse_mode='Markdown')
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg'))
        bot.send_message(message.chat.id, "Вам нужно зарегестрироваться, для этого нажмите кнопку ниже", reply_markup=markup)


    # mail = imaplib.IMAP4_SSL('imap.gmail.com')
    # mail.login('xde.test.070', '6c7c6b7b7x')
    # mail.select("INBOX")
    # (retcode, messages) = mail.search(None, '(UNSEEN)')
    # if retcode == 'OK':
    #     n = 0
    #     for num in messages[0].split():
    #         n = n + 1
    #         typ, data = mail.fetch(num, '(RFC822)')
    #         for respone_part in data:
    #             if isinstance(respone_part, tuple):
    #                 original = email.message_from_string('respone_part[1]')
    #                 print(original['From'])
    #                 data = original['Subject']
    #                 print(data)
    #                 typ, data = mail.store(num, '+FLAGS', '\\Seen')
            

                    
    # bot.send_message(message.chat.id,mail)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за выбор нашего бота!')
    answer = ''
    if call.data == 'reg':
        answer = 'Вы выбрали пункт Зарегистрироваться!\nПожалуйста, введите Ваш email'
        message = bot.send_message(call.message.chat.id, answer)
        bot.register_next_step_handler(message, singup)

    elif call.data == 'more':
        answer = 'Вы выбрали пункт Подробнее про бота!'
    elif call.data == 'say':
        answer = 'Вы выбрали пункт Сказать идею!'
    elif call.data == 'owner':
        answer = 'Перемещаю вас на главную страницу!'
    elif call.data == 'view_all':
        answer = 'Посмотреть всё'
    elif call.data == 'mark_read':
        answer = 'Отметить прочитанным'
    elif call.data == 'answer':
        answer = 'Ответить'
    elif call.data == 'delete':
        answer = 'Удалить'

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)



bot.polling(none_stop = True)