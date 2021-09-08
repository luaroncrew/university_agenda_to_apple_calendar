import logging

from settings import SETTINGS
from extractor import extract_events_from_pdf


def get_setup():
    logging.info('getting setup')
    setup_file = open('vcalendar_setup.ics', mode='r')
    setup = setup_file.read()
    logging.info(f'current setup is \n {setup}')
    setup_file.close()
    return setup


def get_events():
    if SETTINGS['EXTRACTING_FROM_PDF']:
        return extract_events_from_pdf()

    events = []
    count = int(input('enter the amount of events you want to add'))
    for k in range(count):
        event = dict()
        event['title'] = str(input('enter the name of new event'))
        event['date'] = str(input('enter the date of event  like this <YYYYMMDD> 20210925'))
        event['start_time'] = str(input('enter the start time like this <HHMMSS> 093000'))
        event['end_time'] = str(input('enter the start time like this <HHMMSS> 153000'))
        events.append(event)

    return events









