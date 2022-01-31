from .helpers import (np, list_compare, random, is_valid)

class Baseline():    
    def __init__(self, grid, netlist):
        
        self.netlist = netlist
        self.gates = grid.gate_dict
        self.grid = grid

        self.used_lines = []

    def move(self, start, destination):
        """
        returns one step move in random direction if possible, else returns np.array of zeroes
        """

        # make sure we don't cross gates in our path
        forbidden_gates = set(self.gates.values()) - {destination}

        start = np.array(start)
        destination = np.array(destination)

        # don't move if we are at our destination
        if np.array_equal(start, destination):
            return(np.array((0,0,0)))
        
        # go over moves in all directions in random order
        axes = random.sample(range(3), 3)
        for axis in axes:
            directions = random.sample([-1, 1], 2)
            for direction in directions:
                adjustment = np.array((0,0,0))
                adjustment[axis] = direction

                if is_valid(start, adjustment, self.used_lines, forbidden_gates, self.grid):
                    # print(is_valid(start, adjustment, self.used_lines, forbidden_gates, self.grid))
                    return adjustment

        return np.array((0,0,0))

    def solve(self):
        netlist = self.netlist.connections
        connection_path_dict = {}

        for connection in netlist:

            # get gates and their coordinates
            gate_a = connection[0]
            gate_b = connection[1]

            # retrieve gate coordinates as tuples
            coords_gate_a = self.gates[gate_a]
            coords_gate_b = self.gates[gate_b]
            
            # start at gate_a and build a path from gate_a to gate_b
            step = np.array(coords_gate_a)
            path = [coords_gate_a]

            while True:
                print(type(step))
                print(type(coords_gate_b))
                adjustment = self.move(step, coords_gate_b)

                comparison = adjustment == np.array((0,0,0))
                if comparison.all() == True:
                    break

                next_step = tuple(step + adjustment)
                line = {tuple(step), next_step}
                self.used_lines.append(line)
                path.append(next_step)
                step = next_step
            
            connection_path_dict[connection] = path

        return connection_path_dict