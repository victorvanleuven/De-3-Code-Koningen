"""
first algorithm based on the baseline, but avoiding overlap and even intersections by utilising upper layers
"""
from .helpers import (np, list_compare, random, is_valid)


INTERSECTION_PENALTY = 30000
WRONG_LINE_PENALTY = 1000
    

def greedy_cost_move(start, destination, used_lines, grid):
    all_gates = set(grid.gate_dict.values())
    forbidden_gates = set(all_gates) - {destination}

    start = np.array(start)
    destination = np.array(destination)

    if list_compare(start, destination):
        return(np.array((0,0,0)))
    
    points_used = []

    for line in used_lines:
        for point in line:
            points_used.append(point)
    points_used = set(points_used)
    
    weights = []
    adjustments = []

    for axis in range(3):

        adjustment_cost = 1

        for direction in [-1, 1]:
            adjustment = np.array((0,0,0))
            adjustment[axis] = direction
            line = {tuple(start), tuple(start + adjustment)}
            if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
                if list_compare(start + adjustment, destination):
                    return adjustment
                adjustments.append(adjustment)

                # give penalty for making intersections and drifting away from our destination
                if tuple(start + adjustment) in points_used:
                    adjustment_cost += INTERSECTION_PENALTY
                if start[axis] < destination[axis] and direction == -1:
                    adjustment_cost += WRONG_LINE_PENALTY
                elif start[axis] > destination[axis] and direction == 1:
                    adjustment_cost += WRONG_LINE_PENALTY

                weights.append(1/adjustment_cost)
            
    if len(adjustments) == 0:
        return np.array((0,0,0))

    return random.choices(adjustments, weights, k=1)[0]

def greedy_cost(netlist, grid):
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
            adjustment = greedy_cost_move(step, coords_gate_b, used_lines, grid)

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


    