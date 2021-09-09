import smtplib
import os
import logging
from dotenv import load_dotenv


load_dotenv()

DESTINATION = os.getenv('DESTINATION')
PASSWORD = os.getenv('EMAIL_PASSWORD')
LOGIN = os.getenv('EMAIL_LOGIN')

sent_from = LOGIN
to = DESTINATION
subject = 'OMG Super Important Message'
body = 'YO ITS MAIL'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(LOGIN, PASSWORD)
server.sendmail(sent_from, to, email_text)
server.close()
logging.info('mail sent')


