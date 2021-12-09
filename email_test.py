# -*- encoding: utf-8 -*-
from html.parser import HTMLParser

from email import message
from loguru import logger
import email
import base64
import imaplib

import re


class emailCheck():
    def __init__(self, email, password, server):
 
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(email, password)
                
        self.mail.list()
        self.mail.select("inbox")
    
    def decode_text(self, text):
        if text.count('=?UTF-8?B'):
            text = text.replace('=?UTF-8?B', '')
            return base64.b64decode(text).decode('utf-8')
        else:
            return text

    def get_email(self):
        result, data = self.mail.search(None, "ALL")
        email_list = []
        
        id_list = data[0].split()
        
        if result == "OK":
            for item in id_list:
                result, data_email = self.mail.fetch(item, "(RFC822)")
                raw_email = data_email[0][1]
                raw_email_string = raw_email.decode('utf-8')

                email_message = email.message_from_string(raw_email_string)
                email_list.append({
                    'date_send': email_message['Date'],
                    'subject': self.decode_text(email_message['Subject']),
                    'sender': (self.decode_text(email.utils.parseaddr(email_message['From'])[0]), self.decode_text(email.utils.parseaddr(email_message['From'])[1])),
                    'type': 'new'
                    })
        return email_list

    def get_body_email(self, sender, date):
        result, data = self.mail.search(None, "ALL")
        email_list = []
        
        id_list = data[0].split()
        
        if result == "OK":
            item_message = None
            for item in id_list:
                result, data_email = self.mail.fetch(item, "(RFC822)")
                raw_email = data_email[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                if email_message['Date'] == date and self.decode_text(email.utils.parseaddr(email_message['From'])[1]) in sender:
                    item_message = email_message
                    break

        if item_message:
            if email_message.is_multipart():
                payload = email_message.get_payload()[0]
                body = payload.get_payload(decode=True).decode('utf-8')
            else:    
                body = email_message.get_payload(decode=True).decode('utf-8')

            email_body =  re.sub(r'<.*?>', '', body)
            return email_body
        
                
    def delted_email(self, sender, date):
        result, data = self.mail.search(None, "ALL")
        
        id_list = data[0].split()
        
        if result == "OK":
            mail_id = None
            for item in id_list:
                result, data_email = self.mail.fetch(item, "(RFC822)")
                raw_email = data_email[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                if email_message['Date'] == date and self.decode_text(email.utils.parseaddr(email_message['From'])[1]) in sender:
                    mail_id = email_message['Message-Id']
                    break
        logger.debug(mail_id)
        if mail_id:
            self.mail.store(str(mail_id), '+X-GM-tk.LabelS', '\\Trash')
            return True
        else:
          return False