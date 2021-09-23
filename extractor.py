from openpyxl import load_workbook
import settings


# settings
weekday_letters = settings.WEEKDAY_LETTERS
START_TIME = 8


wb = load_workbook('examp.xlsx', data_only=True)
sh = wb['Semaine 38 - 2021']


def lesson_in_my_agenda(lesson) -> bool:
    """
    Filtering function.
    if cell's content is your lesson, returns True
    """

    content = lesson.split()
    # TODO: make smart filtering when you only need to choose your group
    groups_to_exclude = ['STID-1-1', 'STID-1-11', 'STID-1-12', 'STID-1-22']
    for group in groups_to_exclude:
        if (group in content) or (len(content) < 6):
            return False
    return True


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


def read_agenda(sheet) -> list:
    """
    reading excel files to extract events from them,
    returns list of dicts containing event information:
    time, summary, date
    """
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

        # TODO: try to extract the cabinet number

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