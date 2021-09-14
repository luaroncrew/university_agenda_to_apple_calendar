from openpyxl import load_workbook
import settings


wednesday_letters = settings.SETTINGS['WEDNESDAY_LETTERS']

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


def read_agenda(sheet):
    events = []
    needed_ranges = []
    ranges = sheet.merged_cells.ranges
    for cell_range in ranges:
        coordinate = str(cell_range).split(':')
        content = sheet[coordinate[0]].value
        # instead of using try for non-type cells
        if content is None:
            continue
        if lesson_in_my_agenda(content):
            needed_ranges.append(cell_range)

    for event_range in needed_ranges:
        read_cell_indexes = str(event_range).split(':')

        print(read_cell_indexes)

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

        start_time = stringify_time(start_time)
        end_time = stringify_time(end_time)






read_agenda(sh)