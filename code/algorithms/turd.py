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
        self.overlapping_lines = []
        self.solved = self.solve()

    def hill_climber(self):
        pass

    def move(self, step, end, local_used_lines, start):

        forbidden_gates = set(self.gates.values()) - set(end)

        adjustments = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        probabillities = {}
        
        for adjustment in adjustments:
            if is_valid(step, adjustment, local_used_lines, forbidden_gates, self.grid):
                print(local_used_lines)
                probabillities[adjustment] = 1 # score
        
        if len(probabillities) == 0:
            return np.array((0, 0, 0))

        normalized_probabilities = [p/sum(probabillities.values()) for p in probabillities.values()]
        random_index = np.random.choice(len(probabillities), p=normalized_probabilities)
        adjustment = adjustments[random_index]

        return np.array(adjustment)

    def solve(self):
        connection_path_dict = {}
        gates = self.gates

        for connection in self.netlist.connections:
            start = np.array(gates[connection[0]])
            end = np.array(gates[connection[1]])
            local_used_lines = []

            step = start
            path = [step]

            while True:
                adjustment = self.move(step, end, local_used_lines, start)
                path.append(tuple(step + adjustment))
                self.used_lines.append({tuple(step), tuple(step + adjustment)})
                local_used_lines.append({tuple(step), tuple(step + adjustment)})
                
                if np.array_equal(step + adjustment, end):
                    break

                step = step + adjustment
            
            connection_path_dict[connection] = path

        return connection_path_dict 