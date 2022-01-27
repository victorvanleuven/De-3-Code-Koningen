"""
Third algorithm generates a non valid solution with a connections but with overlap. Then by hill climbing generates a valid low-cost solution.
"""
from .helpers import (np, list_compare, random, is_valid, list_remove)

class Test2_algorithm():
    def __init__(self, netlist, grid):
        # input moet dict zijn, met gate_nr = key en coordinaten van gate in tuple
        self.gate_dict = self.load_grid(source_file)
        # n: x, y

    

    def hill_climber(connection_path_dict, overlapping_lines, used_lines, grid):
