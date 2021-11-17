from loguru import logger
from imap_tools import MailBox, AND


pop3server = 'imap.gmail.com'
username = 'web.korzhov@gmail.com'
password = r'umi7q9%%'

# get email bodies from INBOX 
with MailBox(pop3server).login(username, password, 'INBOX') as mailbox:
    for msg in mailbox.fetch():
        body = msg.text or msg.html