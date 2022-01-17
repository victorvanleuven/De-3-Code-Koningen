import csv
from ast import literal_eval
from code.helpers.projection import project_three_d


def load_output(filename_output):
    paths = []

    with open(filename_output) as file:
        csvreader = csv.reader(file, delimiter=',')

        # skips headers of csv
        next(csvreader)

        for row in csvreader:
            if "(" != row[0][0]:
                break
            coordinates = literal_eval(row[1])
            coordinates = map(project_three_d, coordinates)
            paths.append(coordinates)
    
    return paths