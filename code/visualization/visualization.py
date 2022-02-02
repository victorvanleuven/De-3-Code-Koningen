import matplotlib.pyplot as plt
from code.classes.grid import (Grid, project_three_d)
import csv
from ast import literal_eval


def load_output(filename_output):
    """
    turns csv of a solution into a list of paths that can be plotted in visualize
    """
    paths = []

    with open(filename_output) as file:
        csvreader = csv.reader(file, delimiter=",")

        # skips headers of csv
        next(csvreader)

        for row in csvreader:
            if "(" != row[0][0]:
                break
            coordinates = literal_eval(row[1])
            coordinates = map(project_three_d, coordinates)
            paths.append(coordinates)

    return paths


def visualize_grid(filename_visualization, filename_grid, filename_solution):
    """
    this program makes a 3d plot of the gates and their connections provided by their respective csv files
    """

    grid = Grid(filename_grid)
    gates = grid.gate_dict
    for key in gates.keys():
        x = gates[key][0]
        y = gates[key][1]

    paths = load_output(filename_solution)

    ax = plt.figure().add_subplot(projection="3d")
    for path in paths:
        x_list = []
        y_list = []
        z_list = []
        for coord in path:
            x_list.append(coord[0])
            y_list.append(coord[1])
            z_list.append(coord[2])

        if len(gates.keys()) < 20:
            for key in gates.keys():
                x = gates[key][0]
                y = gates[key][1]
                ax.plot(x, y, 0, ".")
                ax.text(x, y, 0, key)
        ax.plot(x_list, y_list, z_list)

    ax.set_zticks(range(8))
    plt.savefig(filename_visualization)
