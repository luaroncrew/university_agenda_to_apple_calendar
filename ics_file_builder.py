import logging
import os

from exporter import send_calendar


def create_calendar(setup, events):
    # creating new calendar file
    calendar = open('calendar.ics', mode='w')

    # adding our setup to calendar
    calendar.write(setup)

    # sending calendar to mail
    send_calendar(calendar)

    # closing and deleting temp calendar file
    calendar.close()
    os.remove('calendar.ics')
