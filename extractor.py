from openpyxl import load_workbook
import settings


wednesday_letters = settings.SETTINGS['WEDNESDAY_LETTERS']

wb = load_workbook('example.xlsx', data_only=True)
sh = wb['Semaine 37 - 2021']


def lesson_in_my_agenda(lesson):
    content = lesson.split()
    groups_to_exclude = ['STID-1-1', 'STID-1-11', 'STID-1-12']
    for group in groups_to_exclude:
        if (group in content) or (len(content) < 5):
            return False
    return True


def read_agenda(sheet):
    ranges = sheet.merged_cells.ranges
    for cell_range in ranges:
        coordinate = str(cell_range).split(':')
        content = sheet[coordinate[0]].value
        # instead of using try for non-type cells
        if content is None:
            continue
        if lesson_in_my_agenda(content):
            print(content.split())


read_agenda(sh)