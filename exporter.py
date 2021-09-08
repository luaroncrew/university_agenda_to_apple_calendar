# this file will be sending all the data by mail

import random
import os


def send_calendar(calendar):
    uid = random.randint(1, 21312312)
    with open(f'debug/cal{uid}') as log:
        log.write(calendar)

    return True
