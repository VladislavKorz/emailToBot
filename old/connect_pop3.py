from loguru import logger
import poplib
import email
from base64 import b64decode

pop3server = 'pop.gmail.com'
username = 'web.korzhov@gmail.com'
password = r'umi7q9%%'

pop3_server = 'pop.gmail.com'
pop3_port = '995'

M = poplib.POP3_SSL(pop3_server, pop3_port)
M.user(username)
M.pass_(password)

numMessages = len(M.list()[1])

def decode_header(header):
    decoded_bytes, charset = email.header.decode_header(header)[0]
    if charset is None:
        return str(decoded_bytes)
    else:
        return decoded_bytes.decode(charset)


for i in range(numMessages):

    raw_email  = b"\n".join(M.retr(i+1)[1])
    parsed_email = email.message_from_bytes(raw_email)
    
    # logger.info(parsed_email)
    print('=========== email #%i ============' % i)
    print('От:', parsed_email['From'])
    print('Дата:', parsed_email['Date'])
    print('Тема:', decode_header(parsed_email['Subject']))
    print('======== email #%i ended =========' % i)


    # soup = BeautifulSoup(parsed_email)
    # print(soup.get_text())