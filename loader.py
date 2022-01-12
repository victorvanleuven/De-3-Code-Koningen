import csv
from ast import literal_eval


filename_grid = "data/gates&netlists/example/print_0.csv"
filename_netlist = "data/gates&netlists/example/netlist_1.csv"
filename_output = "example/output.csv"


def load_netlist(filename_netlist):
    netlist = []
    
    # output kan het beste een string blijven voor overzichtelijkheid 

    with open(filename_netlist) as file:
        csvreader = csv.reader(file, delimiter=',')

        # skipping headers of csv
        next(csvreader)

        for row in csvreader:
            row = tuple(row)
            netlist.append(row)
        return(netlist)


def load_grid(filename_grid):
    gate_coord_dict = {}

    with open(filename_grid) as file:
        csvreader = csv.reader(file, delimiter=',')

        # skips headers of csv
        next(csvreader)

        for row in csvreader:
            gate = row[0]
            coordinates = tuple(row[1:])

            coordinates_int = tuple(map(int, coordinates))
            
            gate_coord_dict[gate] = coordinates_int

        return (gate_coord_dict)


def load_output(filename_output):
    paths = []

    with open(filename_output) as file:
        csvreader = csv.reader(file, delimiter=',')

        # skips headers of csv
        next(csvreader)

        for row in csvreader:
            if "chip" in row[0]:
                break
            coordinates = literal_eval(row[1])
            paths.append(coordinates)
    
    return (paths)


