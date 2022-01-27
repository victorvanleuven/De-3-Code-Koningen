"""
Third algorithm generates a non valid solution with a connections but with overlap. Then by hill climbing generates a valid low-cost solution.
"""
from matplotlib.pyplot import grid
import numpy as np
from .helpers import list_compare, random, is_valid, list_remove

class Test2_algorithm():    
    def __init__(self, grid, netlist):
        
        self.netlist = netlist
        self.grid = grid

        self.used_lines = []
        self.overlapping_lines
        self.solved = self.solve()

    def hill_climber(self):
        pass

    def move(self):
        pass

    def solve(self):
        connection_path_dict = {}
        gates = self.grid.gate_dict

        for connection in self.netlist:
            start = np.array(gates[connection[0]])
            end = np.array(gates[connection[1]])

            step = start
            path = [step]

            while True:
                adjustment = self.move()
                path.append(step + adjustment)
                self.used_lines.append((step), (step + adjustment))
                
                if np.array_equal(step + adjustment, end):
                    break
            
            connection_path_dict[connection] = path

        return connection_path_dict 