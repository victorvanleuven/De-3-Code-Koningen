"""
first algorithm based on the baseline, but avoiding overlap and even intersections by utilising upper layers
"""
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
            if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
                return adjustment
        elif start[direction] < destination[direction]:
            adjustment[direction] += 1
            if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
                return adjustment

    # if we can't move more towards our destination, force to go other valid direction
    directions = np.random.choice(range(3),3,replace=False, p=[1/9,1/9,98/100])
    for direction in directions:
        adjustment = np.array((0,0,0))
        adjustment[direction] = 1
        if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
            return adjustment

    return np.array((0,0,0))

def solve(netlist, grid):
    """
    keep on making the move that minimizes the distance to our destination, choose randomly between best moves
    """
    netlist = netlist.connections
    gates = grid.gate_dict
    connection_path_dict = {}
    used_lines = []
    netlist_counter = 0
    layer_to_use = len(connection_path_dict.keys()) // 10

    for connection in netlist:
        
        netlist_counter += 1

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

            adjustment = move(step, coords_gate_b, used_lines, grid)

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