"""
first algorithm based on the baseline, but avoiding overlap and even intersections by utilising upper layers
"""
from .helpers import (np, list_compare, random, is_valid)

def move(start, destination, used_lines, grid, layer_to_use):
    
    all_gates = set(grid.gate_dict.values())
    forbidden_gates = set(all_gates) - {destination}

    start = np.array(start)
    destination = np.array(destination)
    arrived = 0

    if list_compare(start, destination):
        return(np.array((0,0,0)))

    if start[0] == destination[0] and start[1] == destination[1]:
        adjustment = np.array((0,0,0))
        adjustment[2] -= 1
        arrived = 1
        if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
            return adjustment

    if start[2] < layer_to_use and arrived != 1:
        adjustment = np.array((0,0,0))
        adjustment[2] += 1
        if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
            return adjustment

    directions = np.random.choice(range(3),3,replace=False, p=[50/101,50/101,1/101])
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
    directions = np.random.choice(range(3),3,replace=False, p=[5/11,5/11,1/11])
    for direction in directions:
        adjustment = np.array((0,0,0))
        adjustment[direction] = 1
        if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
            return adjustment
        
        # when path is at destination but too high
        if start[0] == destination[0] and start[1] == destination[1] and start[2] != destination[2]:
            wiggle_list = [-1, 1]
            wiggle = random.choice(wiggle_list)
            adjustment[direction] = wiggle
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
    netlist_counter = 0
    iteration_count = 0
    tries = 0

    for connection in netlist:
        iteration_count += 1
        print("length")
        print(len(netlist))
        print("iteration")
        print(iteration_count)

        netlist_counter += 1
        layer_to_use = netlist_counter // 10

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
            
            # create a list of all values in used lines
            used_lines_values = used_lines.values()
            used_lines_list = []
            for sublist in used_lines_values:
                for item in sublist:
                    used_lines_list.append(item)


            adjustment = move(step, coords_gate_b, used_lines_list, grid, layer_to_use)

            # try the same step 24 times
            if type(adjustment) != np.ndarray and tries < 25:
                tries += 1
                continue
            
            # try the whole path again after 24 times trying the same step
            if type(adjustment) != np.ndarray:
                # path.clear()
                path = [coords_gate_a]
                step = np.array(coords_gate_a)
                used_lines[connection] = []

                # after 100 times trying the path reset every path and start again at the path that was stuck
                if tries == 100:
                    tries = 0
                    used_lines = {}
                    for connection in connection_path_dict.keys():
                        netlist.append(connection)


                    # insert current connection to next spot in netlist to try again
                    netlist.insert(iteration_count - 1, connection)
                    connection_path_dict.clear()
                    netlist_counter = 0
                    continue
                tries += 1
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