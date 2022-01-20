"""
first algorithm based on the baseline, but avoiding overlap and even intersections by utilising upper layers
"""

import numpy as np
import random

LAYERS = 7

def check_max_value(coord, grid):
    max_min_xy = grid.get_maxmin_xy()

    if max_min_xy["max_x"] + 1 < coord[0] or max_min_xy["min_x"] - 1 > coord[0]:
        return False
    elif max_min_xy["max_y"] + 1 < coord[1] or max_min_xy["min_y"] - 1 > coord[1]:
        return False
    elif coord[2] > LAYERS or coord[2] < 0:
        return False
    
    return True

def list_compare(list1, list2):
    comparison = list1 == list2
    return comparison.all()

def list_in(list, list_of_lists):
        for other_list in list_of_lists:
            if list_compare(list, other_list):
                return True
        return False

def greedy_move(start, destination, used_lines, grid):
    
    all_gates = set(grid.gate_dict.values())
    forbidden_gates = set(all_gates) - {destination}

    start = np.array(start)
    destination = np.array(destination)

    if list_compare(start, destination):
        return(np.array((0,0,0)))

    directions = random.sample(range(3), 3)
    for direction in directions:
        adjustment = np.array((0,0,0))
        if start[direction] > destination[direction]:
            adjustment[direction] -= 1
            line = {tuple(start), tuple(start + adjustment)}
            if not line in used_lines and not list_in(start + adjustment, forbidden_gates) and check_max_value(start + adjustment, grid):
                return adjustment
        elif start[direction] < destination[direction]:
            adjustment[direction] += 1
            line = {tuple(start), tuple(start + adjustment)}
            if not line in used_lines and not list_in(start + adjustment, forbidden_gates) and check_max_value(start + adjustment, grid):
                return adjustment

    # if we can't move more towards our destination, force to go other valid direction
    directions = random.sample(range(3), 3)
    for direction in directions:
        adjustment = np.array((0,0,0))
        adjustment[direction] = 1
        line = {tuple(start), tuple(start + adjustment)}
        if not line in used_lines and not list_in(start + adjustment, forbidden_gates) and check_max_value(start + adjustment, grid):
            return adjustment

    return np.array((0,0,0))

def actualsolvecircuit(netlist, grid):
    netlist = netlist.connections
    gates = grid.gate_dict
    connection_path_dict = {}
    used_lines = []

    for connection in netlist:

        # get gates and their coordinates
        gate_a = connection[0]
        gate_b = connection[1]

        # retrieve gate coordinates as tuples
        coords_gate_a = gates[gate_a]
        coords_gate_b = gates[gate_b]
        
        # start at gate_a and build a path from gate_a to gate_b
        step = np.array(coords_gate_a)
        path = [coords_gate_a]

        while True:
            adjustment = greedy_move(step, coords_gate_b, used_lines, grid)

            comparison = adjustment == np.array((0,0,0))
            if comparison.all() == True:
                break

            next_step = tuple(step + adjustment)
            line = {tuple(step), next_step}
            used_lines.append(line)
            path.append(next_step)
            step = next_step
        
        connection_path_dict[connection] = path

    return connection_path_dict