from .helpers import is_valid
import numpy as np


class Greedy_Random:
    """
    algorithm which is greedy with respect to the manhattan distance and chooses randomly between moves of same value
    """

    def __init__(self, grid, netlist):
        self.netlist = netlist
        self.gates = grid.gate_dict
        self.grid = grid
        self.used_lines = []

    def move(self, start, destination):
        """
        if there are moves that bring us closer to our destination choose randomly between them,
        otherwise choose randomly between other directions
        """
        start = np.array(start)
        destination = np.array(destination)

        # stop if we have arrived at our destination
        if np.array_equal(start, destination):
            return np.array((0, 0, 0))

        # avoid all gates except our destination
        forbidden_gates = set(self.gates.values()) - {tuple(destination)}

        # iterate over directions in random order and search for a good move
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

        # if no valid moves were possible, return zero adjustment
        return np.array((0, 0, 0))

    def solve(self):
        """
        tries to realise connections one by one by making greedy random moves
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

                # go to next connection if no moves are possible or if we arrived at our destination
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
