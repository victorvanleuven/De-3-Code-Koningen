from .helpers import is_valid
import numpy as np
import random
import time


class Greedy_Random_2:
    """
    algorithm based on the greedy random algorithm, which forces paths to upper layers
    """

    def __init__(self, grid, netlist):
        self.netlist = netlist
        self.gates = grid.gate_dict
        self.grid = grid

        # keep track of path sorted by connections
        self.used_lines_dict = {}
        self.arrived_xy = False

    def move(self, start, destination, layer_to_use, used_lines):
        """
        first goes up to layer to use and then makes greedy random moves at given layer
        """
        start = np.array(start)
        destination = np.array(destination)

        # stop if we have arrived at our destination
        if np.array_equal(start, destination):
            adjustment = np.array((0, 0, 0))
            return adjustment

        # avoid all gates except our destination
        forbidden_gates = set(self.gates.values()) - {tuple(destination)}

        # first go up to given layer
        if start[2] < layer_to_use and not self.arrived_xy:
            adjustment = np.array((0, 0, 0))
            adjustment[2] += 1
            if is_valid(start, adjustment, used_lines, forbidden_gates, self.grid):
                return adjustment

        # when have arrived at x,y values of destination, try to move down
        if start[0] == destination[0] and start[1] == destination[1]:
            adjustment = np.array((0, 0, 0))
            adjustment[2] -= 1
            self.arrived_xy = True
            if is_valid(start, adjustment, used_lines, forbidden_gates, self.grid):
                return adjustment

        # move to our destination greedy randomly
        directions = np.random.choice(
            range(3), 3, replace=False, p=[50 / 101, 50 / 101, 1 / 101]
        )
        for direction in directions:
            adjustment = np.array((0, 0, 0))
            if start[direction] > destination[direction]:
                adjustment[direction] -= 1
                if is_valid(start, adjustment, used_lines, forbidden_gates, self.grid):
                    return adjustment
            elif start[direction] < destination[direction]:
                adjustment[direction] += 1
                if is_valid(start, adjustment, used_lines, forbidden_gates, self.grid):
                    return adjustment

        # if we can't move more towards our destination, force to go other valid direction
        directions = np.random.choice(
            range(3), 3, replace=False, p=[5 / 11, 5 / 11, 1 / 11]
        )
        for direction in directions:
            adjustment = np.array((0, 0, 0))
            adjustment[direction] = 1
            if is_valid(start, adjustment, used_lines, forbidden_gates, self.grid):
                return adjustment

            # when path is at destination but too high, make random moves
            if (
                start[0] == destination[0]
                and start[1] == destination[1]
                and start[2] != destination[2]
            ):
                wiggle_list = [-1, 1]
                wiggle = random.choice(wiggle_list)
                adjustment[direction] = wiggle
                if is_valid(start, adjustment, used_lines, forbidden_gates, self.grid):
                    return adjustment

        return np.array((0, 0, 0))

    def solve(self):
        """
        try to make connections, if we get stuck at a connection, try again
        if we cannot manage to make the connection in 100 tries, delete all paths and start over,
        beginning at the connection where we got stuck
        """
        connection_path_dict = {}
        netlist_counter = 0
        iteration_count = 0
        tries = 0

        # divide total runtime by connections
        start_time = time.time()
        runtime = 3600 / 70

        for connection in self.netlist.connections:
            iteration_count += 1
            netlist_counter += 1

            # use approximately one layer per 10 connections
            layer_to_use = netlist_counter // 10

            # get gates and their coordinates
            gate_a = connection[0]
            gate_b = connection[1]

            # retrieve gate coordinates as tuples
            coords_gate_a = self.gates[gate_a]
            coords_gate_b = self.gates[gate_b]

            # start at gate_a and build a path from gate_a to gate_b
            step = np.array(coords_gate_a)
            path = [coords_gate_a]

            while time.time() - start_time < runtime:
                print(iteration_count)

                # go to new connections if we have arrived
                if np.array_equal(step, coords_gate_b):
                    break

                # create a list of all used lines
                used_lines = [
                    item
                    for sublist in self.used_lines_dict.values()
                    for item in sublist
                ]

                adjustment = self.move(step, coords_gate_b, layer_to_use, used_lines)

                # try the whole path again when stuck
                if np.array_equal(adjustment, np.array((0, 0, 0))):
                    path = [coords_gate_a]
                    step = np.array(coords_gate_a)
                    self.used_lines_dict[connection] = []

                    # after 100 times trying the path reset every path and start again at the path that was stuck
                    if tries == 100:
                        tries = 0
                        self.used_lines_dict = {}
                        for connection in connection_path_dict.keys():
                            self.netlist.connections.append(connection)

                        # insert current connection to next spot in netlist to try again
                        self.netlist.connections.insert(iteration_count - 1, connection)
                        connection_path_dict.clear()

                        netlist_counter = 0
                        continue

                    tries += 1
                    continue

                next_step = tuple(step + adjustment)
                line = {tuple(step), next_step}

                self.used_lines_dict.setdefault(connection, []).append(line)
                path.append(next_step)
                step = next_step

            connection_path_dict[connection] = path

        return connection_path_dict
