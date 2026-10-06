import sys


"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###

data = parse_nyt_data('data/covid/us-counties.csv')

print('===== Harrisonburg city =====')

rows = []
for entry in data:
    if entry[1] == 'Harrisonburg city' and entry[2] == 'Virginia':
        rows.append((entry[0], entry[4]))

# Question 1
for date, cases in rows:
    if cases > 0:
        print('First case:', date)
        break

# Daily new cases
daily = []
previous = 0
for date, cases in rows:
    daily.append((date, cases - previous))
    previous = cases

# Question 2
best_date = ''
best_cases = -1
for date, new_cases in daily:
    if new_cases > best_cases:
        best_cases = new_cases
        best_date = date
print('Most new cases in one day:', best_date, 'with', best_cases)

# Question 3
best_total = -1
best_start = ''
best_end = ''
for i in range(len(daily) - 6):
    total = 0
    for j in range(i, i + 7):
        total = total + daily[j][1]
    if total > best_total:
        best_total = total
        best_start = daily[i][0]
        best_end = daily[i + 6][0]
print('Worst 7-day period:', best_start, 'to', best_end, 'with', best_total, 'new cases')

print()

print('===== Rockingham County =====')

rows = []
for entry in data:
    if entry[1] == 'Rockingham' and entry[2] == 'Virginia':
        rows.append((entry[0], entry[4]))

# Question 1
for date, cases in rows:
    if cases > 0:
        print('First case:', date)
        break

# Daily new cases
daily = []
previous = 0
for date, cases in rows:
    daily.append((date, cases - previous))
    previous = cases

# Question 2
best_date = ''
best_cases = -1
for date, new_cases in daily:
    if new_cases > best_cases:
        best_cases = new_cases
        best_date = date
print('Most new cases in one day:', best_date, 'with', best_cases)

# Question 3
best_total = -1
best_start = ''
best_end = ''
for i in range(len(daily) - 6):
    total = 0
    for j in range(i, i + 7):
        total = total + daily[j][1]
    if total > best_total:
        best_total = total
        best_start = daily[i][0]
        best_end = daily[i + 6][0]
print('Worst 7-day period:', best_start, 'to', best_end, 'with', best_total, 'new cases')