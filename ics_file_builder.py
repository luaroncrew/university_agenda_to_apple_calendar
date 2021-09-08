import logging
import os
import random

from data_collector import get_events
from exporter import send_calendar
from settings import SETTINGS


def create_calendar(setup):
    # creating new calendar file
    if SETTINGS['DEBUG']:
        destination = f'/debug/{random.randint(1, 120301283)}.ics'
    else:
        destination = 'calendar.ics'

    calendar = open(destination, mode='w')

    # adding our setup to calendar
    calendar.write(setup)

    # getting and creating vevents for calendar
    events = get_events()
    for event in events:
        vevent_string = str()
        vevent_string += 'BEGIN:VEVENT\n'
        vevent_string += 'DTSTAMP:20210904T194914Z\n'  # here we have to add a custom date
        vevent_string += f'DTSTART;TZID=Europe/Paris:{event["date"]}T{event["start_time"]}'
        vevent_string += f'DTEND;TZID=Europe/Paris:{event["date"]}T{event["end_time"]}'
        vevent_string += f'SUMMARY:{event["title"]}'
        vevent_string += 'END:VEVENT'

    # writing closing calendar tag to file before returning it
    calendar.write('END:VCALENDAR')

    # closing calendar, exporting it and deleting temp calendar file
    calendar.close()
    send_calendar(calendar)
    os.remove('calendar.ics')
