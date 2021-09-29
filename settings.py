# settings

SETTINGS = {
    'EXTRACTING_FROM_FILE': True,
    'DEBUG': True,
}

# this variable contains 5 lists of letters, each list for one weekday
WEEKDAY_LETTERS = [
    list('BCDEFGHI'),
    list('JKLMNOPQ'),
    list('RSTUVWXY'),
    ['Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG'],
    ['AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
]

POSSIBLE_CABINET_NUMBERS = [
    'Am1', 'Am2'
]

ALL_GROUP_NAMES = [
    'STID-1-1',
    'STID-1-2',
    'STID-1-11',
    'STID-1-12',
    'STID-1-21',
    'STID-1-22',
    'STID-1-ECO-1',
    'STID-1-ECO-2',
    'STID-1-MATH',
    'STID-1-INFO-1',
    'STID-1-INFO-2'
]

USERS_GROUPS = [
    'STID-1-2',
    'STID-1-21',
    'STID-1-ECO-2',
    'STID-1-MATH'
]


def get_groups_to_exclude():
    groups_to_exclude = ALL_GROUP_NAMES
    [groups_to_exclude.remove(item) for item in USERS_GROUPS]
    return groups_to_exclude
