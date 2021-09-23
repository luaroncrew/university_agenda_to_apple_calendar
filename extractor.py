import logging

# TODO: implement pytest
# TODO: set logging
from openpyxl import load_workbook
import settings


weekday_letters = settings.WEEKDAY_LETTERS

# TODO: try loading workbooks list
wb = load_workbook('examp.xlsx', data_only=True)
sh = wb['Semaine 38 - 2021']
START_TIME = 8


def lesson_in_my_agenda(lesson):
    content = lesson.split()
    groups_to_exclude = ['STID-1-1', 'STID-1-11', 'STID-1-12', 'STID-1-22']
    for group in groups_to_exclude:
        if (group in content) or (len(content) < 6):
            return False
    return True


def stringify_date(date: str):
    logging.debug(f'object{date} received')
    date_elements = date.split('/')
    string_date = date_elements[2] + date_elements[1] + date_elements[0]
    return string_date


def stringify_time(time):
    hours = str(int(time))
    minutes = '30' if time % 1 != 0 else '00'
    return hours + minutes + '00'


def get_date(cell_range, dates):
    # getting first letter
    cell_main_letter = str(cell_range)[0]

    # adding second letter if exists
    if str(cell_range)[1].isalpha():
        cell_main_letter += str(cell_range)[1]

    # filtering
    for index, letters in enumerate(weekday_letters):
        if cell_main_letter in letters:
            return dates[index]


# FIXME: make it load the needed excel file for execution from main
def read_agenda(sheet):
    dates = []
    needed_ranges = []

    # getting ranges to treat
    ranges = sheet.merged_cells.ranges

    # filtering ranges
    for cell_range in ranges:
        coordinate = str(cell_range).split(':')
        content = sheet[coordinate[0]].value

        # instead of using try for non-type cells
        if content is None:
            continue

        # checking if value is number
        if isinstance(content, int):
            continue

        # checking if lesson is for my group
        if lesson_in_my_agenda(content):
            needed_ranges.append(cell_range)

        # checking if cell range is date
        if len(content.split('/')) >= 3:
            dates.append(cell_range)

    # sometimes there are some additional dates in agenda, they must be deleted
    if len(dates) > 5:
        for k in range(len(dates)-5):
            dates.pop()

    print(dates)
    for date in dates:
        cell_index = str(date).split(':')[0]
        print(sheet[cell_index].value)
    events = []

    # reading ranges with their times
    for event_range in needed_ranges:
        read_cell_indexes = str(event_range).split(':')

        # reading start time cell index
        start_time = str()
        for element in read_cell_indexes[0]:
            if element.isdigit():
                start_time += element

        # reading end time cell index
        end_time = str()
        for element in read_cell_indexes[1]:
            if element.isdigit():
                end_time += element

        start_time = START_TIME + (int(start_time) - 8) / 2
        end_time = START_TIME + (int(end_time) - 8) / 2 + 0.5

        event_start_time = stringify_time(start_time)
        event_end_time = stringify_time(end_time)

        # reading date
        date_cell = get_date(event_range, dates)
        date = sheet[str(date_cell).split(':')[0]].value
        event_date = stringify_date(date)

        # getting summary
        summary = sheet[read_cell_indexes[0]].value

        event = {
            'date': event_date,
            'start_time': event_start_time,
            'end_time': event_end_time,
            'title': summary.split('\n')[0]
        }

        events.append(event)

    return events


if __name__ == '__main__':
    print(read_agenda(sh))