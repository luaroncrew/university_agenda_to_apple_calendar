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
subject = 'OMG Super Important Message'
body = 'ssshhhiiittt'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, to, subject, body)

logging.info('connection opened')
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(LOGIN, PASSWORD)
server.sendmail(sent_from, to, email_text)
server.close()
logging.info('mail sent')


