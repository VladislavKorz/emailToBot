from loguru import logger
import time
from bd.commands import get_user_all, user_login
from email_work import emailCheck
from config import bot
from telebot import types

def start_mail():
    logger.info('Hello')
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
            
            @bot.callback_query_handler(func=lambda call: True)
            def query_handler(call):
                logger.info(call.message.chat.id)
                answer = ''
                if call.data == 'reg':
                    answer = 'Вы выбрали пункт Зарегистрироваться!\nПожалуйста, введите Ваш email'
                    message = bot.send_message(call.message.chat.id, answer)
                    bot.register_next_step_handler(message, singup)

                elif call.data == 'more':
                    answer = 'Вы выбрали пункт Подробнее про бота!'
                elif call.data == 'say':
                    answer = 'Вы выбрали пункт Сказать идею!'
                    bot.send_message(call.message.chat.id,"Наша идея заключается в автоматизации бизнес процесса нефтегазовой промышленности посредством нашего телеграм-бота!")
                elif call.data == 'owner':
                    answer = 'Перемещаю вас на главную страницу!'
                    bot.send_message(call.message.chat.id,"Бот,который берёт сообщения из email сервисов и отправляет в Telegram группу сотрудников компании!")
                elif call.data == 'view_all':
                    answer = 'Посмотреть всё'
                elif call.data == 'mark_read':
                    answer = 'Отметить прочитанным'
                elif 'email_otvet_' in call.data:
                    answer = 'Ответить'
                    to = (call.data).replace('email_otvet_', '')
                    user = user_login(call.message.chat.id)
                    msg = emailCheck(user[0], user[1], user[2]).send_mail(to, 'Answer for message')
                    bot.edit_message_text('Мы отправили ответ этому адресу:\n'+str(to), chat_id=call.message.chat.id, message_id=call.message.message_id)
                elif 'email_view' in call.data:
                    bot.answer_callback_query(callback_query_id=call.id, text='Мы готовы показать Вам письмо, но сначала посчитайте до 5!')
                    uid = (call.data).replace('email_view_', '')
                    user = user_login(call.message.chat.id)
                    msg = emailCheck(user[0], user[1], user[2]).get_body_email(uid)
                    answer = f'Письмо просмотрено'
                    bot.edit_message_text(call.message.text+'\n\nВот что Вам написали в письме:\n'+str(msg), chat_id=call.message.chat.id, message_id=call.message.message_id)
                elif 'email_delete' in call.data:
                    answer = f'Письмо удалено'
                    uid = (call.data).replace('email_delete_', '')
                    user = user_login(call.message.chat.id)
                    msg = emailCheck(user[0], user[1], user[2]).delted_email(uid)
                    bot.edit_message_text("Письмо удалено", chat_id=call.message.chat.id, message_id=call.message.message_id)

                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        except:
            logger.error('Произошла ошибка, надо что-то исправить в проверке почты')
             