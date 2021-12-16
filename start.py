# import time
# from threading import Thread

# def sleepMe(i):
#     print("Поток %i засыпает на 5 секунд.\n" % i)
#     time.sleep(5)
#     print("Поток %i сейчас проснулся.\n" % i)

# for i in range(10):
#     th = Thread(target=sleepMe, args=(i, ))
#     th.start()
# Import smtplib for the actual sending function

import smtplib
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login('xde.test.070@gmail.com','1029384756bot')
to = 'korzhov.vladd@gmail.com'
email = 'xde.test.070@gmail.com'
msg = 'Helllooooo'
message = f"From: From Person {email}\nTo: To Person {to}\nSubject: Sending SMTP e-mail\n{msg}"

smtpObj.sendmail("xde.test.070@gmail.com","korzhov.vladd@gmail.com",message)
smtpObj.quit()