from openpyxl import load_workbook

from extractor import read_agenda


# setting up testing files
wb1 = load_workbook('test_example_1.xlsx', data_only=True)
worksheet_1 = wb1['Semaine 38 - 2021']

wb2 = load_workbook('test_example_2.xlsx', data_only=True)
worksheet_2 = wb2['Semaine 37 - 2021']


def test_read_agenda_count():
    """
    checking if reading algorithm returns all the events
    """
    assert len(read_agenda(worksheet_1)) == 16
    assert len(read_agenda(worksheet_2)) == 15
