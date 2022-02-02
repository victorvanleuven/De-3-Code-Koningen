from code.algorithms.greedy_random_2_0 import Greedy_Random_2
from .helpers import list_compare, is_valid
import numpy as np


class Greedy_Random_Hillclimber:
    """
    algorithm generates a non valid solution with a connections but with overlap,
    then by hill climbing generates a solution with less overlap
    """
    def __init__(self, grid, netlist):
        self.netlist = netlist
        self.gates = grid.gate_dict
        self.grid = grid
        self.max_values = grid.get_maxmin_xy()
        self.arrived_xy = False
        self.tries = 0
        self.used_lines = {}

    def find_overlap(self, connection_path_dict):
        """
        find overlapping lines per connection
        """
        lines_dict = {}
        checked_lines = []
        overlapping_lines_dict = {}

        # creates used lines from used points in a connection path
        for connection in connection_path_dict:
            lines = []
            points = connection_path_dict[connection]
            for index in range(len(connection_path_dict[connection]) - 1):
                a = points[index]
                b = points[index + 1]
                line = {a, b}
                lines.append(line)
            lines_dict[connection] = lines

        # find overlapping lines per connection
        for connection in lines_dict:
            for line in lines_dict[connection]:
                if line in checked_lines:
                    overlapping_lines_dict.setdefault(connection, []).append(line)
                else:
                    checked_lines.append(line)

        return overlapping_lines_dict

    def move(self, start, destination, local_used_lines):
        """
        performs greedy random move (but now is only called with used lines of current path in solve)
        """
        start = np.array(start)
        destination = np.array(destination)

        if list_compare(start, destination):
            return np.array((0, 0, 0))

        forbidden_gates = set(self.gates.values()) - {tuple(destination)}
        directions = np.random.choice(
            range(3), 3, replace=False, p=[50 / 101, 50 / 101, 1 / 101]
        )
        for direction in directions:
            adjustment = np.array((0, 0, 0))
            if start[direction] > destination[direction]:
                adjustment[direction] -= 1
                if is_valid(start, adjustment, local_used_lines, forbidden_gates, self.grid):
                    return adjustment
            elif start[direction] < destination[direction]:
                adjustment[direction] += 1
                if is_valid(start, adjustment, local_used_lines, forbidden_gates, self.grid):
                    return adjustment

        # if we can't move more towards our destination, force to go other valid direction
        directions = np.random.choice(
            range(3), 3, replace=False, p=[1 / 9, 1 / 9, 7 / 9]
        )
        for direction in directions:
            adjustment = np.array((0, 0, 0))
            adjustment[direction] = 1
            if is_valid(start, adjustment, local_used_lines, forbidden_gates, self.grid):
                return adjustment

        return np.array((0, 0, 0))

    def hill_climber(self, connection_path_dict):
        """
        given solution with overlap, tries connections with overlap again using greedy random 2.0
        """
        while self.tries < 500:
            # get overlapping lines per connection
            overlapping_lines_dict = self.find_overlap(connection_path_dict)
            
            # stop if there is no more overlap
            overlapping_lines_list = [
                item for sublist in overlapping_lines_dict.values() for item in sublist
            ]
            if len(overlapping_lines_list) == 0:
                break
            
            # try connections with overlap again using greedy random 2.0
            for connection in overlapping_lines_dict:
                if connection not in overlapping_lines_dict:
                    continue

                # save old path
                old_overlap = overlapping_lines_dict[connection]
                old_used_lines = self.used_lines[connection]

                # clear current path
                overlapping_lines_dict[connection] = []
                self.used_lines[connection] = []

                # randomly assign a layer for greedy random 2.0 to use
                layer_to_use = np.random.choice(range(1, 8))

                start = self.gates[connection[0]]
                destination = self.gates[connection[1]]
                step = start
                path = [start]
                
                while True:
                    used_lines_list = [
                        item for sublist in self.used_lines.values() for item in sublist
                    ]

                    adjustment = Greedy_Random_2.move(
                        self, step, destination, layer_to_use, used_lines_list
                    )

                    # set to old path when stuck and go to next connection
                    if np.array_equal(adjustment, np.array((0, 0, 0))):
                        overlapping_lines_dict[connection] = old_overlap
                        self.used_lines[connection] = old_used_lines
                        self.tries += 1
                        break

                    # make path
                    line = {tuple(step), tuple(step + adjustment)}
                    self.used_lines[connection].append(line)
                    step = step + adjustment
                    path.append(tuple(step))

                    # stop if destination reached
                    if np.array_equal(step, destination):
                        connection_path_dict[connection] = path
                        overlapping_lines_dict = self.find_overlap(connection_path_dict)
                        break
                    
        return connection_path_dict

    def solve(self):
        """
        ignore overlap, keep on making the move that minimizes the distance to our destination, 
        choose randomly between best moves
        """
        netlist = self.netlist.connections
        gates = self.gates
        connection_path_dict = {}

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
                adjustment = self.move(step, coords_gate_b, local_used_lines)

                if np.array_equal(adjustment, np.array((0, 0, 0))):
                    break

                next_step = tuple(step + adjustment)
                line = {tuple(step), next_step}

                self.used_lines.setdefault(connection, []).append(line)
                local_used_lines.append(line)

                path.append(next_step)
                step = next_step

            connection_path_dict[connection] = path

        # apply hill climber algorithm to current solution
        solution = self.hill_climber(connection_path_dict)

        return solution
