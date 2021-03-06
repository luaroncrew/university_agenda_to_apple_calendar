import datetime
from openpyxl import load_workbook

import settings


# settings
weekday_letters = settings.WEEKDAY_LETTERS
possible_cabinet_numbers = settings.POSSIBLE_CABINET_NUMBERS
all_group_names = settings.ALL_GROUP_NAMES
groups_to_exclude = settings.get_groups_to_exclude()
START_TIME = 8


wb = load_workbook('test_example_3.xlsx', data_only=True)
sh = wb.worksheets[0]


def get_cells_letter(cell_range):
    """
    supporting function for better sorting dates, returns cell's range letter index.
    if it contains 2 letters, returns 'Z' + letter to release sorting
    """
    cell_letter = str()
    range_first_coordinate = str(cell_range).split(':')[0]
    for letter in range_first_coordinate:
        if letter.isalpha():
            cell_letter += letter

    if len(cell_letter) == 2:
        cell_letter = 'Z' + cell_letter[1]

    return cell_letter


def lesson_in_my_agenda(lesson) -> bool:
    """
    Filtering function.
    if cell's content is your lesson, returns True
    """
    content = lesson.split()
    for group in groups_to_exclude:
        if group in content:
            return False
    return True


def is_users_lesson(content) -> bool:
    """
    if cell's content looks like a lesson, check by another function if lesson is for
    user's group. Finally it will return true or false whether it must be in user's agenda
    or not
    """
    # checking if it's a lesson
    elements = content.split()
    for element in elements:
        if element in ['TD', 'TP', 'CM']:
            return lesson_in_my_agenda(content)

    if len(content.split()) >= 6:
        return lesson_in_my_agenda(content)
    return False


def stringify_date(date: str) -> str:
    """
    returns date in appropriate way for agenda
    """
    date_elements = date.split('/')
    string_date = date_elements[2] + date_elements[1] + date_elements[0]
    return string_date


def stringify_time(time) -> str:
    """
    returns time in appropriate way for agenda
    """
    hours = str(int(time))
    if len(hours) == 1:
        hours = '0' + hours
    minutes = '30' if time % 1 != 0 else '00'
    return hours + minutes + '00'


def get_date(cell_range, dates):
    """
    comparing merged cell's first letter to weekday letters from settings,
    if date is found for the letter, return date connected to the cell
    """
    # getting first letter
    cell_main_letter = str(cell_range)[0]

    # adding second letter if exists
    if str(cell_range)[1].isalpha():
        cell_main_letter += str(cell_range)[1]

    # filtering
    for index, letters in enumerate(weekday_letters):
        if cell_main_letter in letters:
            return dates[index]


def extract_cabinet_number(lesson: str):
    """
    takes merged cell's text as param and returns the cabinet number from it by filtering or None if
    it doesn't exist
    """
    for element in lesson.split():
        # filtering
        if len(element.split('-')) == 2:
            if len(element.split('-')[0]) == 1:
                if len(element.split('-')[1]) == 3:
                    return element
        if element in possible_cabinet_numbers:
            return element

    return None


def read_agenda(sheet) -> list:
    """
    reading excel files to extract events from them,
    returns list of dicts containing event information:
    time, summary, date
    """
    dates_ranges = []
    lesson_ranges = []

    # getting ranges to treat
    ranges = sheet.merged_cells.ranges

    # filtering ranges
    for cell_range in ranges:
        coordinate = str(cell_range).split(':')
        content = sheet[coordinate[0]].value

        if content is None:
            continue

        # checking if value is number
        if isinstance(content, int):
            continue

        # checking if lesson is for my group
        if is_users_lesson(content):
            lesson_ranges.append(cell_range)

        # checking if cell range is date
        if (len(content.split('/')) >= 3) and (len(content.split(' ')) < 2):
            dates_ranges.append(cell_range)

    # making datetime objects out of str-dates to sort and then revert
    dates = []
    for cell_range in dates_ranges:
        dates.append(sheet[str(cell_range).split(':')[0]].value)

    dates = [datetime.datetime.strptime(date, '%d/%m/%Y') for date in dates]
    dates.sort(reverse=True)
    dates = [date.strftime('%d/%m/%Y') for date in dates]

    # sometimes there are some additional dates_ranges in agenda, they must be deleted
    if len(dates) > 5:
        for k in range(len(dates) - 5):
            dates.pop()

    for cell_range in dates_ranges:
        if sheet[str(cell_range).split(':')[0]].value not in dates:
            dates_ranges.remove(cell_range)

    # to avoid mixing dates we have to sort the cells
    dates_ranges = sorted(dates_ranges, key=get_cells_letter)

    events = []
    # reading ranges with their times
    for event_range in lesson_ranges:
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
        date_cell = get_date(event_range, dates_ranges)
        date = sheet[str(date_cell).split(':')[0]].value
        event_date = stringify_date(date)

        contents = sheet[read_cell_indexes[0]].value
        # getting summary
        summary = contents.split('\n')[0]

        # extracting cabinet number
        location = extract_cabinet_number(contents)

        # TODO: write a function that extracts teacher's name

        event = {
            'date': event_date,
            'start_time': event_start_time,
            'end_time': event_end_time,
            'title': summary,
            'location': location
        }

        events.append(event)

    return events


if __name__ == '__main__':
    print(read_agenda(sh))
