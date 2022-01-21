import argparse
from code.classes.circuit import Circuit
import csv
import code.visualisation.visualization as visualization
from code.classes.netlist import Netlist
from code.classes.grid import Grid
from code.algorithms.baseline import solve_circuit_baseline
from code.algorithms.cost_first_algoritm import actualsolvecircuit
import time

def evaluate(connection_path_dict, grid):
    gate_dict = grid.gate_dict
    counter = 0
    for connection in connection_path_dict.keys():
        end = gate_dict[connection[1]]
        path = connection_path_dict[connection]
        if path[-1][0] == end[0] and path[-1][1] == end[1] and path[-1][2] == end[2]:
            counter += 1
    return counter

def check(connection_path_dict, grid):
    gate_dict = grid.gate_dict
    for connection in connection_path_dict.keys():
        end = gate_dict[connection[1]]
        path = connection_path_dict[connection]
        if path[-1][0] != end[0] or path[-1][1] != end[1] or path[-1][2] != end[2]:
            return False
    return True

def main(grid_file, netlist_file, output, visualisation):
    t0 = time.time()
    "usage: python3 main.py data/example/print_0.csv data/example/netlist_1.csv test/test.csv test/test.png"
    grid_name = grid_file
    netlist_name = netlist_file
    netlist = Netlist(netlist_file)
    grid = Grid(grid_file)

    # try a 1000 times, pick correct solution with lowest cost
    lowest_cost = 10000000000000
    most_connections = 0
    best_solution = []
    for tries in range(10000):
        print(tries)
        solved = actualsolvecircuit(netlist, grid)

        connections_made = evaluate(solved, grid)
        if connections_made >= most_connections:
            most_connections = connections_made
            cost = Circuit(solved).cost()
            if cost < lowest_cost:
                lowest_cost = cost
                best_solution.clear()
                best_solution.append(solved)

    t1 = time.time()
    print(t1 - t0)    
    if len(best_solution) == 0:
        print("No solution found")
        return 0
        
    connections_made = evaluate(best_solution[0], grid)
    print(f"Reached {connections_made} connections")

    
    solved = best_solution[0]
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