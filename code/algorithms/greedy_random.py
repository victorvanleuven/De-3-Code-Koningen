"""
first algorithm based on the baseline, but avoiding overlap and even intersections by utilising upper layers
"""
from .helpers import np, is_valid


class Greedy_Random:
    def __init__(self, grid, netlist):

        self.netlist = netlist
        self.gates = grid.gate_dict
        self.grid = grid

        self.used_lines = []

    def move(self, start, destination):

        forbidden_gates = set(self.gates.values()) - {destination}

        start = np.array(start)
        destination = np.array(destination)

        if np.array_equal(start, destination):
            return np.array((0, 0, 0))

        directions = np.random.choice(
            range(3), 3, replace=False, p=[50 / 101, 50 / 101, 1 / 101]
        )
        for direction in directions:
            adjustment = np.array((0, 0, 0))
            if start[direction] > destination[direction]:
                adjustment[direction] -= 1
                if is_valid(
                    start, adjustment, self.used_lines, forbidden_gates, self.grid
                ):
                    return adjustment
            elif start[direction] < destination[direction]:
                adjustment[direction] += 1
                if is_valid(
                    start, adjustment, self.used_lines, forbidden_gates, self.grid
                ):
                    return adjustment

        # if we can't move more towards our destination, force to go other valid direction
        directions = np.random.choice(
            range(3), 3, replace=False, p=[1 / 9, 1 / 9, 7 / 9]
        )
        for direction in directions:
            adjustment = np.array((0, 0, 0))
            adjustment[direction] = 1
            if is_valid(start, adjustment, self.used_lines, forbidden_gates, self.grid):
                return adjustment

        return np.array((0, 0, 0))

    def solve(self):
        """
        keep on making the move that minimizes the distance to our destination, choose randomly between best moves
        """
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
                adjustment = self.move(step, coords_gate_b)

                comparison = adjustment == np.array((0, 0, 0))
                if comparison.all() == True:
                    break

                next_step = tuple(step + adjustment)
                line = {tuple(step), next_step}
                self.used_lines.append(line)
                path.append(next_step)
                step = next_step

            connection_path_dict[connection] = path

        return connection_path_dict
