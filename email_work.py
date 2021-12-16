from imap_tools import MailBox, AND
from imap_tools import A, AND, OR, NOT
from imap_tools.query import N
from loguru import logger
import smtplib


class emailCheck():
    def __init__(self, email, password, server='imap.gmail.com'):
        self.email = email
        self.password = password
        self.server = server
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
        self.mailbox.delete([msg.uid for msg in self.mailbox.fetch(AND(uid=uid))])
        return 'Сообщение удалено'

    def send_mail(self, to, msg, subject='Новое письмо'):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(self.email,self.password)
        message = f"From: From Person {self.email}\nTo: To Person {to}\nSubject: {subject}\n{msg}"
        # message = """From: From Person %s  
        # To: To Person %s  
        # Subject: %s 
        # %s
        # """%(self.email,to, subject, msg) 
        smtpObj.sendmail(self.email, to, message)
        smtpObj.quit()