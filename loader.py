import csv
import sys

filename_grid = "data/gates&netlists/chip_0/print_0.csv"
filename_netlist = "data/gates&netlists/chip_0/netlist_1.csv"

def main():
    load_netlist(filename_netlist)
    load_grid(filename_grid)

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
        print(netlist)


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
        print(gate_coord_dict)


main()