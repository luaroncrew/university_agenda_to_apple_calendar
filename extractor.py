from openpyxl import load_workbook
import settings


weekday_letters = settings.WEEKDAY_LETTERS


wb = load_workbook('example.xlsx', data_only=True)
sh = wb['Semaine 37 - 2021']
START_TIME = 8


def lesson_in_my_agenda(lesson):
    content = lesson.split()
    groups_to_exclude = ['STID-1-1', 'STID-1-11', 'STID-1-12', 'STID-1-22']
    for group in groups_to_exclude:
        if (group in content) or (len(content) < 6):
            return False
    return True


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

        # checking if lesson is for my group
        if lesson_in_my_agenda(content):
            needed_ranges.append(cell_range)

        # checking if cell range is date
        if len(content.split('/')) >= 3:
            dates.append(cell_range)

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
        date = sh[str(date_cell).split(':')[0]].value
        summary = sh[read_cell_indexes[0]].value

        print(event_start_time, event_end_time, date, summary)




read_agenda(sh)
