import csv
from ast import literal_eval


filename_grid = "data/gates&netlists/example/print_0.csv"
filename_netlist = "data/gates&netlists/example/netlist_1.csv"
filename_output = "example/output.csv"

# maakt van 2d coordinaten (tuple) 3d coordinaten door een 0 toe te voegen.
def project_three_d(coord):
    if len(coord) == 2:
        coord += (0,)
    return coord

def load_netlist(filename_netlist):
    netlist = []

    with open(filename_netlist) as file:
        csvreader = csv.reader(file, delimiter=',')

        # skipping headers of csv
        next(csvreader)

        for row in csvreader:
            row = tuple(map(int, row))
            netlist.append(row)
        return(netlist)


def load_grid(filename_grid):
    gate_coord_dict = {}

    with open(filename_grid) as file:
        csvreader = csv.reader(file, delimiter=',')

        # skips headers of csv
        next(csvreader)

        for row in csvreader:
            gate = int(row[0])
            coordinates = tuple(row[1:])

            coordinates_int = tuple(map(int, coordinates))
            
            gate_coord_dict[gate] = project_three_d(coordinates_int)
        
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
            coordinates = map(project_three_d, coordinates)
            paths.append(coordinates)
    
    return (paths)
