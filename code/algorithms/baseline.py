from .helpers import (np, list_compare, random, is_valid)

def move(start, destination, used_lines, grid):
    """
    returns one step move in random direction if possible, else returns np.array of zeroes
    """

    # make sure we don't cross gates in our path
    all_gates = set(grid.gate_dict.values())
    forbidden_gates = set(all_gates) - {destination}

    start = np.array(start)
    destination = np.array(destination)

    # don't move if we are at our destination
    if list_compare(start, destination):
        return(np.array((0,0,0)))
    
    # go over moves in all directions in random order
    axes = random.sample(range(3), 3)
    for axis in axes:
        directions = random.sample([-1, 1], 2)
        for direction in directions:
            adjustment = np.array((0,0,0))
            adjustment[axis] = direction

            if is_valid(start, adjustment, used_lines, forbidden_gates, grid):
                return adjustment

    return np.array((0,0,0))

def solve(netlist, grid):
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