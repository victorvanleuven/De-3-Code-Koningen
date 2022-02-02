import argparse
from code.classes.circuit import Circuit
import csv
import code.visualization.visualization as visualization
from code.classes.netlist import Netlist
from code.classes.grid import Grid
from code.algorithms import (
    baseline,
    greedy_random,
    greedy_random_2_0,
    greedy_random_hillclimber as gr_h,
)
from typing import Callable
import time


def count_connections(connection_path_dict, grid):
    """
    returns number of connections that are realized
    """
    gate_dict = grid.gate_dict
    counter = 0
    for connection in connection_path_dict.keys():
        end = gate_dict[connection[1]]
        path = connection_path_dict[connection]
        if path[-1][0] == end[0] and path[-1][1] == end[1] and path[-1][2] == end[2]:
            counter += 1
    return counter


def count_overlap(connection_path_dict):
    """
    returns number of overlapping lines
    """
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


def main(chip, netlist, algorithm_name: Callable, runtime, batchruns):
    # gather data from batchruns into one list of dictionaries
    batch_dict_list = []
    for batch in range(batchruns):

        grid_file = f"data/{chip}/print_{chip[-1]}.csv"
        netlist_file = f"data/{chip}/{netlist}.csv"

        grid = Grid(grid_file)
        lowest_cost = 10000000000000
        least_overlap = 1000000
        most_connections = 0
        best_solution = None

        # translate user input to desired algorithm
        algo_dict = {
            "baseline": baseline.Baseline,
            "gr": greedy_random.Greedy_Random,
            "gr_2": greedy_random_2_0.Greedy_Random_2,
            "gr_hill": gr_h.Greedy_Random_Hillclimber,
        }
        algorithm = algo_dict[algorithm_name]

        start = time.time()
        n_runs = 0
        while time.time() - start < runtime:
            print(n_runs)

            solved = algorithm(grid, Netlist(netlist_file)).solve()
            cost = Circuit(solved).cost()
            connections_made = count_connections(solved, grid)
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

        output = f"test/{netlist}/{algorithm_name}_{runtime}_[{batch}]_{n_runs}_{overlap}.csv"
        visualisation = f"test/{netlist}/{algorithm_name}_{runtime}_[{batch}]_{n_runs}_{overlap}.png"

        # make solution of current run into csv file and visualize it
        run_dict_list = []
        headers = ["net", "wires"]
        for connection in best_solution.keys():
            new_row = {"net": connection, "wires": best_solution[connection]}
            run_dict_list.append(new_row)
        run_dict_list.append(
            {"net": f"{chip}_{netlist[0:3]+netlist[-2:]}", "wires": lowest_cost}
        )
        with open(output, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(run_dict_list)

        # make visualisation of current run
        visualization.visualize_grid(visualisation, grid_file, output)

        # add data of current run to csv of all batchruns
        batch_headers = ["runs", "connections", "cost", "overlap"]
        batch_row = {"runs": n_runs, "connections": most_connections, "cost": lowest_cost, "overlap": least_overlap}
        batch_dict_list.append(batch_row)
        batch_file = f"test/batchruns/{netlist}_{algorithm_name}_{runtime}.csv" 
        with open(batch_file, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=batch_headers)
            writer.writeheader()
            writer.writerows(batch_dict_list)


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
    parser.add_argument("batchruns", type= int, help="number of batchruns")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(
        args.chip_file,
        args.netlist_file,
        args.algorithm,
        args.runtime,
        args.batchruns,
    )
