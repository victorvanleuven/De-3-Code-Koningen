import argparse
from code.classes.circuit import Circuit
import csv
import code.visualisation.visualization as visualization
from code.classes.netlist import Netlist
from code.classes.grid import Grid
from code.algorithms.baseline import solvecircuit_baseline

def main(grid_file, netlist_file, output, visualisation):
    "usage: python3 main.py data/example/print_0.csv data/example/netlist_1.csv test/test.csv test/test.png"
    grid_name = grid_file
    netlist_name = netlist_file
    netlist = Netlist(netlist_file)
    grid = Grid(grid_file)

    solved = solvecircuit_baseline(netlist, grid)
    circuit = Circuit(solved)
    headers = ["net", "wires"]

    grid_name_csv = grid_name.split("/")[0]
    netlist_name_csv = netlist_name[:-4].split("/")[1].replace("list","")

    new_dict = []
    for connection in solved.keys():
        new_row = {"net": connection, "wires": solved[connection]}
        new_dict.append(new_row)

    new_dict.append({"net": f"{grid_name_csv}_{netlist_name_csv}", "wires": circuit.cost()})

    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers)
        writer.writeheader()
        writer.writerows(new_dict)

    visualization.visualize_grid(visualisation, grid_name, output)
      
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "Generates connections between gates in a chip with the lowest cost possible.")

    # Adding arguments
    parser.add_argument("print_file", help = "print file (csv)")
    parser.add_argument("netlist_file", help = "netlist file (csv)")
    parser.add_argument("output_file", help = "output file (csv)")
    parser.add_argument("visualisation_file", help = "visualization (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.print_file, args.netlist_file, args.output_file, args.visualisation_file)