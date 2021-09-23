import logging
import os
from dotenv import load_dotenv
from openpyxl import load_workbook

from mail_exporter import send_calendar
from settings import SETTINGS
from extractor import read_agenda

# TODO: make simple tests for main functions

load_dotenv()

# settings
SENDER = os.getenv('EMAIL_LOGIN')
DESTINATION = os.getenv('DESTINATION')
PASSWORD = os.getenv('EMAIL_PASSWORD')

# TODO: try loading workbooks list to automate execution and exclude it from settings
wb = load_workbook('examp.xlsx', data_only=True)
sh = wb['Semaine 38 - 2021']


def get_setup() -> str:
    """
    reading agenda setup and returns it as string
    """

    logging.info('getting setup')
    setup_file = open('vcalendar_setup.ics', mode='r')
    setup = setup_file.read() + '\n'
    setup_file.close()
    return setup


def get_events() -> list:
    # TODO: make excel sheet as param for func

    logging.info('getting events')
    # if user's choice is extracting events from excel file, reading events from excel
    if SETTINGS['EXTRACTING_FROM_FILE']:
        return read_agenda(sh)

    # if we want to add events manually, this part of function is used
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


def write_events(events: list, calendar):
    """
    takes list of events and calendar file then writes every event in appropriate way to file
    """
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


def create_calendar(setup, calendar_name, events):
    logging.info(f'creating calendar {calendar_name}')

    # creating new calendar file
    calendar = open(calendar_name + '.ics', mode='w')

    # write setup to calendar
    calendar.write(setup)

    # writing events
    write_events(events, calendar)

    # writing closing calendar tag to file before returning it
    calendar.write('END:VCALENDAR\n')

    # closing calendar, exporting it and deleting temp calendar file
    calendar.close()

    # sending calendar to mail from env file
    send_calendar(destination=DESTINATION, sender=SENDER, password=PASSWORD, filename=calendar_name)

    os.remove(calendar_name + '.ics')


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('building started')
    setup = get_setup()
    events = get_events()
    create_calendar(setup, 'agenda', events=events)


if __name__ == '__main__':
    main()
