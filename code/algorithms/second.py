"""
Third algorithm generates a non valid solution with a connections but with overlap. Then by hill climbing generates a valid low-cost solution.
"""
from matplotlib.pyplot import grid
import numpy as np
from .helpers import check_max_value, is_almost_valid, list_compare, random, is_valid, list_remove

class Second():    
    def __init__(self, grid, netlist):
        
        self.netlist = netlist
        self.gates = grid.gate_dict
        self.grid = grid
        self.max_values = grid.get_maxmin_xy()


        self.used_lines = []
        self.overlapping_lines
        self.solved = self.solve()

    def hill_climber(self):
        pass

    def move(self, step, end, start):


        probabillities = [1, 1, 1, 1, 95, 1]
        adjustments = [np.array((1, 0, 0)), np.array((-1, 0, 0)), np.array((0, 1, 0)),
                        np.array((0, -1, 0)), np.array((0, 0, 1)), np.array((0, 0, -1))]
        
        forbidden_gates = set(self.gates.values()) - set(end)

        for direction in range(3):
            adjustment = np.array((0, 0, 0))
            if step[direction] < end[direction]:
                probabillities[0] += 1000
            elif step[direction] > end[direction]:
                return adjustment

        adjustment = np.random.choice(adjustments, 6,replace=False, p=[1/100, 1/100, 1/100, 1/100, 95/100, 1/100])

        for adjustment in adjustments:
            if is_almost_valid(step, adjustment, forbidden_gates, self.grid):
                return adjustment
        
        return np.array((0, 0, 0))
        

    def solve(self):
        connection_path_dict = {}
        gates = self.gates

        for connection in self.netlist:
            start = np.array(gates[connection[0]])
            end = np.array(gates[connection[1]])

            step = start
            path = [step]

            while True:
                adjustment = self.move(step, end, start)
                path.append(step + adjustment)
                self.used_lines.append((step), (step + adjustment))
                
                if np.array_equal(step + adjustment, end):
                    break
            
            connection_path_dict[connection] = path

        return connection_path_dict 