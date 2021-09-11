from openpyxl import load_workbook


wb = load_workbook('example.xlsx', data_only=True)
sh = wb['Semaine 37 - 2021']

print(sh['Z8'].value)


def read_agenda(sheet):
    pass