import email
import imaplib
import base64


mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('xde.test.070@gmail.com', '1029384756bot')
 
mail.list()
mail.select("inbox")

result, data = mail.search(None, "ALL")
 
ids = data[0]
id_list = ids.split()

for latest_email_id in id_list:
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')

    email_message = email.message_from_string(raw_email_string)
    # base64.b64decode(a)
    from_email = email.utils.parseaddr(email_message['From'])[0]
    if from_email.count('=?UTF-8?B'):
        from_email = from_email[len('=?UTF-8?B'):]
        print(base64.b64decode(from_email).decode('utf-8'))


 