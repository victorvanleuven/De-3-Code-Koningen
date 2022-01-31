import argparse
from code.classes.circuit import Circuit
import csv
import code.visualisation.visualization as visualization
from code.classes.netlist import Netlist
from code.classes.grid import Grid
from code.algorithms import baseline, greedy_random, greedy_random_2_0, third_algorithm, turd
from typing import Callable
import datetime
import time


RUNS = 10

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

def count_overlap(connection_path_dict):
    checked_lines = []
    overlap = 0
    used_lines = [item for sublist in connection_path_dict.values() for item in sublist]
    for line in used_lines:
        if line in checked_lines:
            overlap += 1
        else:
            checked_lines.append(line)
    return overlap



def main(chip, netlist, algorithm: Callable, output, visualisation):
    """
    usage: python3 main.py chip_a netlist_b algorithm [output] [visualisation]
    
    choose one of the following algorithms: baseline, greedy_random
    output and visualisation are optional and have default file names "test/chip_a_netlist_b_datetime.csv"
    and "test/chip_a_netlist_b_datetime.png" respectively
    """
    timestamp = str(datetime.datetime.now())[5:16]
    if output == None:
        output = f"test/{algorithm}_{chip}_{netlist}[{timestamp}].csv"
    if visualisation == None:
        visualisation = f"test/{algorithm}_{chip}_{netlist}[{timestamp}].png"


    grid_file = f"data/{chip}/print_{chip[-1]}.csv"
    netlist_file = f"data/{chip}/{netlist}.csv"
    
    grid = Grid(grid_file)
    netlist_to_solve = Netlist(netlist_file)

    # try a 1000 times, pick correct solution with lowest cost
    lowest_cost = 10000000000000
    most_connections = 0
    best_solution = None

    algo_dict = {"baseline": baseline.Baseline, "greedy_random": greedy_random.Greedy_Random, "greedy_random_2": greedy_random_2_0.Greedy_Random_2, "second": turd.Second, "third": third_algorithm.Third}
    algorithm = algo_dict[algorithm]
   
    t0 = time.time()
    
    for run in range(RUNS):
        print("RUN!")
        print(run)

        # print(netlist_to_solve.connections)
        solved = algorithm(grid, Netlist(netlist_file)).solve()

        cost = Circuit(solved).cost()
        least_overlap = 100

        connections_made = evaluate(solved, grid)

        if connections_made > most_connections:
            most_connections = connections_made
            lowest_cost = cost
            best_solution = solved
        if connections_made == most_connections and count_overlap(solved) < least_overlap:          # cost < lowest_cost:
            least_overlap = count_overlap(solved)
            best_solution = solved
    
    print(count_overlap(best_solution))
    if best_solution == None:
        print("No solution found")
        return 0

    connections_made = evaluate(best_solution, grid)
    print(f"Reached {connections_made} connections")
    t1 = time.time()
    print("tijd =")
    print(t1-t0)

    circuit = Circuit(best_solution)
    headers = ["net", "wires"]

    new_dict = []
    for connection in best_solution.keys():
        new_row = {"net": connection, "wires": best_solution[connection]}
        new_dict.append(new_row)

    new_dict.append({"net": f"{chip}_{netlist[0:3]+netlist[-2:]}", "wires": circuit.cost()})

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