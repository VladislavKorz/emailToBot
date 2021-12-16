import time
from threading import Thread

from loguru import logger
from bot_parser import start_bot
from th_chek_email import start_mail


logger.info(f'Старт потоков')
thread1 = Thread(target=start_bot, daemon=True)
thread2 = Thread(target=start_mail, daemon=True)

thread1.start()
thread2.start()

thread1.join()
thread2.join()