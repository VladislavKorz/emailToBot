import imaplib
import email

HOST = 'imap.gmail.com'
USERNAME = 'web.korzhov@gmail.com'
PASSWORD = 'umi7q9%%'

m = imaplib.IMAP4_SSL(HOST, 993)
m.login(USERNAME, PASSWORD)
m.select('INBOX')

def decode_header(header):
    decoded_bytes, charset = email.header.decode_header(header)[0]
    if charset is None:
        return str(decoded_bytes)
    else:
        return decoded_bytes.decode(charset)
        
result, data = m.uid('search', None, "UNSEEN")
if result == 'OK':
    for num in data[0].split()[:5]:
        result, data = m.uid('fetch', num, '(RFC822)')
        if result == 'OK':
            email_message = email.message_from_bytes(data[0][1])
            email_from = str(make_header(decode_header(email_message_raw['From'])))
            # von Edward Chapman -> https://stackoverflow.com/questions/7314942/python-imaplib-to-get-gmail-inbox-subjects-titles-and-sender-name
            subject = str(email.header.make_header(email.header.decode_header(email_message_raw['Subject'])))
            # content = email_message_raw.get_payload(decode=True)
            # von Todor Minakov -> https://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
            # b = email.message_from_string(email_message_raw)
            # this is already set as Message object which have many methods (i.e. is_multipart(), walk(), etc.)
            b = email_message 
            body = ""

            if b.is_multipart():
                for part in b.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))

                    # skip any text/plain (txt) attachments
                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        body = part.get_payload(decode=True)  # decode
                        break
            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
            else:
                body = b.get_payload(decode=True)
                    
m.close()
m.logout()