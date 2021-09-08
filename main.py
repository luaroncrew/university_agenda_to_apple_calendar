import logging

from data_collector import get_setup
from ics_file_builder import create_calendar


def main(email):
    logging.info('reading setup')
    setup = get_setup()
    create_calendar(setup)


if __name__ == '__main__':
    logging.basicConfig(filename='logs.txt', level=logging.INFO)
    logging.info('building started')
    destination_email = input('input your email first')
    main(
        email=destination_email
    )
