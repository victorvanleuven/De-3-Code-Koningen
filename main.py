import argparse
from code.classes.circuit import Circuit
import csv
import code.visualisation.visualization as visualization
from code.classes.netlist import Netlist
from code.classes.grid import Grid
from code.algorithms import (
    baseline,
    greedy_random,
    greedy_random_2_0,
    greedy_random_hillclimber as gr_h,
)
from typing import Callable
import datetime
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


def count_overlap(connection_path_dict):
    checked_lines = []
    lines = []
    overlap = 0
    used_points = connection_path_dict.values()

    for list in used_points:
        for index in range(len(list) - 1):
            a = list[index]
            b = list[index + 1]
            line = {a, b}
            lines.append(line)

    for line in lines:
        if line in checked_lines:
            overlap += 1
        else:
            checked_lines.append(line)

    return overlap


def main(chip, netlist, algorithm_name: Callable, runtime, output, visualisation):
    """
    usage: python3 main.py chip_a netlist_b algorithm [output] [visualisation]

    choose one of the following algorithms: baseline, greedy_random
    output and visualisation are optional and have default file names "test/chip_a_netlist_b_datetime.csv"
    and "test/chip_a_netlist_b_datetime.png" respectively
    """
    golden_dict = []
    batch_runs = 10
    for batch in range(batch_runs):
        timestamp = str(datetime.datetime.now())[5:16]

        grid_file = f"data/{chip}/print_{chip[-1]}.csv"
        netlist_file = f"data/{chip}/{netlist}.csv"

        grid = Grid(grid_file)

        lowest_cost = 10000000000000
        most_connections = 0
        best_solution = None

        algo_dict = {
            "baseline": baseline.Baseline,
            "gr": greedy_random.Greedy_Random,
            "gr_2": greedy_random_2_0.Greedy_Random_2,
            "gr_hill": gr_h.Greedy_Random_Hillclimber,
        }
        algorithm = algo_dict[algorithm_name]

        start = time.time()
        n_runs = 0
        least_overlap = 1000000

    
        while time.time() - start < runtime:
            print(n_runs)

            # print(netlist_to_solve.connections)
            solved = algorithm(grid, Netlist(netlist_file)).solve()

            cost = Circuit(solved).cost()

            connections_made = evaluate(solved, grid)

            overlap = count_overlap(solved)

            # algorithms either make all connections with overlap or avoid overlap but fail to make connections
            # which is why only one of the two conditions has to be checked
            if connections_made > most_connections or overlap < least_overlap:
                most_connections = connections_made
                lowest_cost = cost
                least_overlap = overlap
                best_solution = solved
            elif connections_made == most_connections and overlap == least_overlap:
                if cost < lowest_cost:
                    least_overlap = overlap
                    best_solution = solved
            
            n_runs += 1

        if best_solution == None:
            print("No solution found")
            return 0

        connections_made = evaluate(best_solution, grid)
        print(f"Reached {connections_made} connections")

        circuit = Circuit(best_solution)


        output = f"test/{netlist}/{algorithm_name}_{runtime}_[{batch}]_{n_runs}_{overlap}.csv"
        visualisation = f"test/{netlist}/{algorithm_name}_{runtime}_[{batch}]_{n_runs}_{overlap}.png"
        print(output)

        # make output csv file
        new_dict = []
        headers = ["net", "wires"]
        for connection in best_solution.keys():
            new_row = {"net": connection, "wires": best_solution[connection]}
            new_dict.append(new_row)
        new_dict.append(
            {"net": f"{chip}_{netlist[0:3]+netlist[-2:]}", "wires": circuit.cost()}
        )
        with open(output, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(new_dict)

        # make visualisation file
        visualization.visualize_grid(visualisation, grid_file, output)

        # used for data gathering only, delete later
        golden_headers = ["runs", "overlap"]
        golden_row = {"runs": n_runs, "overlap": overlap}
        golden_dict.append(golden_row)
        golden_file = f"test/{netlist}_{algorithm_name}_{runtime}.csv" 
        with open(golden_file, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=golden_headers)
            writer.writeheader()
            writer.writerows(golden_dict)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(
        description="Generates connections between gates in a chip with the lowest cost possible."
    )

    # Adding arguments
    parser.add_argument("chip_file", help="chip file (csv)")
    parser.add_argument("netlist_file", help="netlist file (csv)")
    parser.add_argument(
        "algorithm",
        help="algorithm to be used: [random_algo, greedy_distance, greedy_cost]",
    )
    parser.add_argument("runtime", type= int, help="runtime in seconds")
    parser.add_argument("output_file", help="output file (csv)", nargs="?")
    parser.add_argument("visualisation_file", help="visualization (png)", nargs="?")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(
        args.chip_file,
        args.netlist_file,
        args.algorithm,
        args.runtime,
        args.output_file,
        args.visualisation_file,
    )
