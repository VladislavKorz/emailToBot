from imap_tools import MailBox, AND
from imap_tools import A, AND, OR, NOT
from imap_tools.query import N
from loguru import logger


class emailCheck():
    def __init__(self, email, password, server='imap.gmail.com'):
        self.mailbox = MailBox(server)
        self.mailbox.login(email, password, initial_folder='INBOX')
    
    def get_email(self):
        email_list = []
        for msg in self.mailbox.fetch(AND(all=True)):
            email_list.append({
                'date_send': msg.date_str,
                'subject': msg.subject,
                'sender': msg.from_,
                'uid': msg.uid,
                })
        return email_list

    def get_body_email(self, uid):
        email_body = None
        for msg in self.mailbox.fetch(AND(uid=uid)):
            email_body = msg.text
        return email_body

    def delted_email(self, uid):
        email_body = None
        for msg in self.mailbox.fetch(AND(uid=uid)):
            email_body = msg.text
        return email_body
