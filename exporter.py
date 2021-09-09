import smtplib
import os
import logging
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logging.info('sending started')
load_dotenv()

DESTINATION = os.getenv('DESTINATION')
PASSWORD = os.getenv('EMAIL_PASSWORD')
LOGIN = os.getenv('EMAIL_LOGIN')

sent_from = LOGIN
to = DESTINATION
subject = 'i hope it doesnt go to spam'
body = 'look what ive done mec'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, to, subject, body)

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
logging.info('connection opened')
server.ehlo()
server.login(LOGIN, PASSWORD)
server.sendmail(sent_from, to, email_text)
server.close()
logging.info('mail sent')


