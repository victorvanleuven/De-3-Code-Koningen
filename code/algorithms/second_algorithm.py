"""
A* algoritme om route met laagste kosten (Circuit.cost()) te vinden, gebaseerd op heuristieken.
Greedy met look ahead
"""

from re import sub
from .helpers import (np, list_compare, random, is_valid)

def move(start, destination, used_lines, grid):
    
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
            if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
                return adjustment
        elif start[direction] < destination[direction]:
            adjustment[direction] += 1
            line = {tuple(start), tuple(start + adjustment)}
            if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
                return adjustment

    # if we can't move more towards our destination, force to go other valid direction
    directions = np.random.choice(range(3),3,replace=False, p=[1/9,1/9,7/9])    # dit ipv random.sample?
    for direction in directions:
        adjustment = np.array((0,0,0))
        adjustment[direction] = 1
        line = {tuple(start), tuple(start + adjustment)}
        if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
            return adjustment

    return 1

def solve(netlist, grid):
    """
    keep on making the move that minimizes the distance to our destination, choose randomly between best moves
    """
    netlist = netlist.connections
    gates = grid.gate_dict
    connection_path_dict = {}
    used_lines = {}

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
        tries = 0

        while True:
            used_lines_values = used_lines.values()
            used_lines_list = []
            for sublist in used_lines_values:
                for item in sublist:
                    used_lines_list.append(item)


            adjustment = move(step, coords_gate_b, used_lines_list, grid)
            
            if type(adjustment) != np.ndarray:
                # path.clear()
                path = [coords_gate_a]
                step = np.array(coords_gate_a)
                used_lines[connection] = []
                used_lines_values = used_lines.values()
                if tries == 100:
                    tries = 0
                    break
                    # netlist.append(connection_path_dict.keys())
                    # connection_path_dict.clear()    
                tries += 1
                # print(tries)
                continue

            comparison = adjustment == np.array((0,0,0))
            if comparison.all() == True:
                break

            next_step = tuple(step + adjustment)
            line = {tuple(step), next_step}

            used_lines.setdefault(connection, []).append(line)
            # used_lines[connection] = line
            path.append(next_step)
            # print(path)
            step = next_step
        
        connection_path_dict[connection] = path


    return connection_path_dict