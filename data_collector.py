import logging

from main import SETTINGS
from extractor import extract_events_from_pdf


def get_setup():
    setup_file = open('vcalendar_setup.ics', mode='r')
    setup = setup_file.read()
    logging.info(f'current setup is \n {setup}')
    setup_file.close()
    return setup


def get_events():
    if SETTINGS['EXTRACT_FROM_PDF']:
        return extract_events_from_pdf()




