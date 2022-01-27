"""
Third algorithm generates a non valid solution with a connections but with overlap. Then by hill climbing generates a valid low-cost solution.
"""
from .helpers import (np, list_compare, random, is_valid, list_remove)


def move(start, destination, used_lines, grid):
    
    all_gates = set(grid.gate_dict.values())
    forbidden_gates = set(all_gates) - {destination}

    start = np.array(start)
    destination = np.array(destination)

    if list_compare(start, destination):
        return(np.array((0,0,0)))

    directions = np.random.choice(range(3),3,replace=False, p=[50/101,50/101,1/101])
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
    directions = np.random.choice(range(3),3,replace=False, p=[1/9,1/9,7/9])
    for direction in directions:
        adjustment = np.array((0,0,0))
        adjustment[direction] = 1
        line = {tuple(start), tuple(start + adjustment)}
        if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
            return adjustment

    return np.array((0,0,0))

def find_line_segments(lines):
    # store every line segment as list of tuples
    line_segments = []

    for line in lines:
        line = list(line)
        points = [line[0], line[1]]
        lines.remove(set(line))
        
        while True:
            for other_line in lines:
                other_line = list(other_line)
                if other_line[0] in points:
                    points.append(other_line[1])
                    lines.remove(set(other_line))
                    continue
                elif other_line[1] in points:
                    points.append(other_line[0])
                    lines.remove(set(other_line))
                    continue
            break
        line_segments.append(points)

    return line_segments



def hill_climber(connection_path_dict, overlapping_lines):

    for connection in overlapping_lines:
        overlap = overlapping_lines[connection]
        old_path = connection_path_dict[connection]
        print(connection)
        print(find_line_segments(overlap))
    
    return connection_path_dict
    


def solve(netlist, grid):
    """
    keep on making the move that minimizes the distance to our destination, choose randomly between best moves
    """
    netlist = netlist.connections
    gates = grid.gate_dict
    connection_path_dict = {}
    used_lines = []
    overlapping_lines = {}

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

        # we don't want path to overlap itself
        local_used_lines = []

        while True:
            adjustment = move(step, coords_gate_b, local_used_lines, grid)

            comparison = adjustment == np.array((0,0,0))
            if comparison.all() == True:
                break

            next_step = tuple(step + adjustment)
            line = {tuple(step), next_step}
            if line in used_lines:
                overlapping_lines.setdefault(connection, []).append(line)
            used_lines.append(line)
            local_used_lines.append(line)
    
            path.append(next_step)
            step = next_step
        
        connection_path_dict[connection] = path

    return hill_climber(connection_path_dict, overlapping_lines)