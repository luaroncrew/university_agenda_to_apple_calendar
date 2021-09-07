import logging
import os

from data_collector import get_events


def create_calendar(setup, events):
    # creating new calendar file
    calendar = open('calendar.ics', mode='w')

    # adding our setup to calendar
    calendar.write(setup)

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


    # closing and deleting temp calendar file
    calendar.close()
    os.remove('calendar.ics')
