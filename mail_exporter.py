import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

SENDER = os.getenv('EMAIL_LOGIN')
DESTINATION = os.getenv('DESTINATION')
PASSWORD = os.getenv('EMAIL_PASSWORD')

msg = MIMEMultipart('This is test mail')

msg['Subject'] = 'Test mail'
msg['From'] = SENDER
msg['To'] = DESTINATION


attachment = open('calendar.ics', "rb")
p = MIMEApplication(attachment.read(), _subtype="ics")
p.add_header('Content-Disposition', "attachment; filename=calendar.ics")
msg.attach(p)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, DESTINATION, msg.as_string())
    logging.info('message sent successfully')
