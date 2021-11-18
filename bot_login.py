import email
from config import bot
from bd.commands import user_create

def singup(message):
    email = message.text

    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, singup_password, email)

def singup_password(message, email):
    password = message.text
    req = user_create(email, message.text, message.from_user.id)
    if 'Create' in req:
        bot.send_message(message.chat.id, 'Пользователь успешно создан')
    elif 'Error' in req:
        bot.send_message(message.chat.id, req)
    else:
        bot.send_message(message.chat.id, f'Ошибка:\n{req}')
