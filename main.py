import argparse
from code.classes.circuit import Circuit
import csv
import code.visualisation.visualization as visualization
from code.classes.netlist import Netlist
from code.classes.grid import Grid
from code.algorithms.baseline import random_algo
from code.algorithms.first_algorithm import greedy_distance
from code.algorithms.cost_first_algoritm import greedy_cost
from typing import Callable
import datetime

TRIES = 100

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


def main(chip_a, netlist_b, algorithm: Callable, output, visualisation):
    """
    usage: python3 main.py chip_a netlist_b algorithm output visualisation
    netlist_b should be in the folder chip_a
    algorithm should be one of the following: random_algo, greedy_distance, greedy_cost
    output and visualisation are optional and have default values "test/chip_a_netlist_b_datetime.csv"
    and "test/chip_a_netlist_b_datetime.png" respectively
    """
    # main(chip_0, netlist_0) optioneel om naam output en visualisation mee te geven, anders gewoon solution_tijd, viz_tijd in results folder?
    
    if output == None:
        output = f"test/{chip_a}_{netlist_b}_{datetime.datetime.now()}.csv"
    if visualisation == None:
        visualisation = f"test/{chip_a}_{netlist_b}_{datetime.datetime.now()}.png"


    grid_file = f"data/{chip_a}/print_{chip_a[-1]}.csv"
    netlist_file = f"data/{chip_a}/{netlist_b}.csv"
    grid = Grid(grid_file)
    netlist = Netlist(netlist_file)

    # try a 1000 times, pick correct solution with lowest cost
    lowest_cost = 10000000000000
    most_connections = 0
    best_solution = None

    algo_dict = {"random_algo": random_algo, "greedy_distance": greedy_distance, "greedy_cost": greedy_cost}
    algorithm = algo_dict[algorithm]
    for tries in range(TRIES):
        print(tries)
        solved = algorithm(netlist, grid)

        connections_made = evaluate(solved, grid)
        if connections_made >= most_connections:
            most_connections = connections_made
            cost = Circuit(solved).cost()
            if cost < lowest_cost:
                lowest_cost = cost
                best_solution = solved
 
    if best_solution == None:
        print("No solution found")
        return 0

    connections_made = evaluate(best_solution, grid)
    print(f"Reached {connections_made} connections")

    circuit = Circuit(best_solution)
    headers = ["net", "wires"]

    new_dict = []
    for connection in best_solution.keys():
        new_row = {"net": connection, "wires": best_solution[connection]}
        new_dict.append(new_row)

    new_dict.append({"net": f"{chip_a}_{netlist_b[0:3]+netlist_b[-2:]}", "wires": circuit.cost()})

    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers)
        writer.writeheader()
        writer.writerows(new_dict)

    visualization.visualize_grid(visualisation, grid_file, output)
      
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "Generates connections between gates in a chip with the lowest cost possible.")

    # Adding arguments
    parser.add_argument("chip_file", help = "chip file (csv)")
    parser.add_argument("netlist_file", help = "netlist file (csv)")
    parser.add_argument("algorithm", help = "algorithm to be used: [random_algo, greedy_distance, greedy_cost]")
    parser.add_argument("output_file", help = "output file (csv)", nargs="?")
    parser.add_argument("visualisation_file", help = "visualization (png)", nargs="?")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.chip_file, args.netlist_file, args.algorithm, args.output_file, args.visualisation_file)