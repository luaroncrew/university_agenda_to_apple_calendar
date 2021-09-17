import logging
import os
from dotenv import load_dotenv

from mail_exporter import send_calendar
from settings import SETTINGS
from extractor import read_agenda


load_dotenv()

SENDER = os.getenv('EMAIL_LOGIN')
DESTINATION = os.getenv('DESTINATION')
PASSWORD = os.getenv('EMAIL_PASSWORD')


def get_setup():
    logging.info('getting setup')
    setup_file = open('vcalendar_setup.ics', mode='r')
    setup = setup_file.read() + '\n'
    logging.info(f'current setup is \n {setup}')
    setup_file.close()
    return setup


def get_events():
    logging.info('getting events from user')
    if SETTINGS['EXTRACTING_FROM_PDF']:

        return

    events = []
    count = int(input('enter the amount of events you want to add'))
    for k in range(count):
        event = dict()
        event['title'] = str(input('enter the name of new event'))
        event['date'] = str(input('enter the date of event  like this <YYYYMMDD> 20210925'))
        event['start_time'] = str(input('enter the start time like this <HHMMSS> 093000'))
        event['end_time'] = str(input('enter the start time like this <HHMMSS> 153000'))
        events.append(event)
    logging.info('events extracted')
    logging.info(f'events:{events}')
    return events


def create_calendar(setup):
    logging.info('creating calendar')

    # creating new calendar file
    destination = 'agenda.ics'
    calendar = open(destination, mode='w')
    logging.info('writing current setup to calendar')

    # adding our setup to calendar
    calendar.write(setup)
    logging.info('setup added')

    # getting and creating vevents for calendar
    events = get_events()
    logging.info('writing events to calendar')
    for event in events:
        vevent_string = str()
        vevent_string += 'BEGIN:VEVENT\n'
        vevent_string += 'DTSTAMP:20210904T194914Z\n'  # here we have to add a custom date
        vevent_string += f'DTSTART;TZID=Europe/Paris:{event["date"]}T{event["start_time"]}\n'
        vevent_string += f'DTEND;TZID=Europe/Paris:{event["date"]}T{event["end_time"]}\n'
        vevent_string += f'SUMMARY:{event["title"]}\n'
        vevent_string += 'END:VEVENT\n'
        calendar.write(vevent_string)
        logging.info(f'event {event["title"]} successfully writen')

    # writing closing calendar tag to file before returning it
    calendar.write('END:VCALENDAR\n')

    # closing calendar, exporting it and deleting temp calendar file
    calendar.close()

    send_calendar(destination=DESTINATION, sender=SENDER, password=PASSWORD)

    os.remove('agenda.ics')


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('building started')
    setup = get_setup()
    create_calendar(setup)


if __name__ == '__main__':
    main()
