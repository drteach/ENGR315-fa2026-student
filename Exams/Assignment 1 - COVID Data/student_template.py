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

data = parse_nyt_data("data/covid/us-counties.csv")


harrisonburg_first_date = ""
rockingham_first_date = ""

for record in data:
    date, county, state, fips, cases, deaths = record

    if state == "Virginia" and cases > 0:
        if county == "Harrisonburg city" and harrisonburg_first_date == "":
            harrisonburg_first_date = date

        if county == "Rockingham" and rockingham_first_date == "":
            rockingham_first_date = date

print("First positive case in Harrisonburg:", harrisonburg_first_date)
print("First positive case in Rockingham County:", rockingham_first_date)

previous_harrisonburg_cases = 0
previous_rockingham_cases = 0
most_harrisonburg_new_cases = -1
most_rockingham_new_cases = -1
harrisonburg_max_date = ""
rockingham_max_date = ""

for record in data:
    date, county, state, fips, cases, deaths = record

    if state == "Virginia" and county == "Harrisonburg city":
        new_cases = cases - previous_harrisonburg_cases
        if new_cases > most_harrisonburg_new_cases:
            most_harrisonburg_new_cases = new_cases
            harrisonburg_max_date = date
        previous_harrisonburg_cases = cases

    if state == "Virginia" and county == "Rockingham":
        new_cases = cases - previous_rockingham_cases
        if new_cases > most_rockingham_new_cases:
            most_rockingham_new_cases = new_cases
            rockingham_max_date = date
        previous_rockingham_cases = cases

print("Date with the most new cases in Harrisonburg:", harrisonburg_max_date)
print("Date with the most new cases in Rockingham County:", rockingham_max_date)