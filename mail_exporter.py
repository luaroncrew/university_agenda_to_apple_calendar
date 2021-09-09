import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_calendar(sender, destination, password):
    msg = MIMEMultipart('Here is your agenda for the next week')
    msg['Subject'] = 'agenda'
    msg['From'] = sender
    msg['To'] = destination
    attachment = open('agenda.ics', "rb")
    p = MIMEApplication(attachment.read(), _subtype="ics")
    p.add_header('Content-Disposition', "attachment; filename=calendar.ics")
    msg.attach(p)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, destination, msg.as_string())
        logging.info('message sent successfully')
