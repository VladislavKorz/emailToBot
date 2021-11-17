from loguru import logger
import poplib
import email

class emailCheck():
    def __init__(self):
        pop3server = 'pop.gmail.com'
        pop3_port = '995'
        username = 'web.korzhov@gmail.com'
        password = r'umi7q9%%'

        self.M = poplib.POP3_SSL(pop3server, pop3_port)
        self.M.user(username)
        self.M.pass_(password)
        
        self.numMessages = len(self.M.list()[1])

        
    def decode_header(self, header):
        decoded_bytes, charset = email.header.decode_header(header)[0]
        if charset is None:
            return str(decoded_bytes)
        else:
            return decoded_bytes.decode(charset)

    def get_email(self):
        email_list = []
        for i in range(self.numMessages):
            raw_email  = b"\n".join(self.M.retr(i+1)[1])
            parsed_email = email.message_from_bytes(raw_email)
            email_list.append({
                'key': i,
                'date_send': parsed_email['Date'],
                'subject': self.decode_header(parsed_email['Subject']),
                'sender': parsed_email['From'],
                'attachments': None,
                'type': 'new'
                })
        return email_list


