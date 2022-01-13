import argparse
import loader
import solve_circuit
from circuit import Circuit
import csv
import visualization

def main(grid, netlist, output, visualisation):
    grid_name = grid
    netlist_name = netlist
    netlist = loader.load_netlist(netlist)
    grid = loader.load_grid(grid)

    solved = solve_circuit.actualsolvecircuit(netlist, grid)
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
    parser.add_argument("print", help = "print file (csv)")
    parser.add_argument("netlist", help = "netlist file (csv)")
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("visualisation", help = "visualization (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.print, args.netlist, args.output, args.visualisation)