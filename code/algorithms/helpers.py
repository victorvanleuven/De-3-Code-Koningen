"""
contains all helper functions used in algorithms
"""

import numpy as np
import random

LAYERS = 7

def check_max_value(coord, grid):
    """
    checks whether given coordinates are between the borders of the grid, assuming 7 layers on top of the chip
    """
    max_min_xy = grid.get_maxmin_xy()

    if max_min_xy["max_x"] + 1 < coord[0] or max_min_xy["min_x"] - 1 > coord[0]:
        return False
    elif max_min_xy["max_y"] + 1 < coord[1] or max_min_xy["min_y"] - 1 > coord[1]:
        return False
    elif coord[2] > LAYERS or coord[2] < 0:
        return False
    
    return True

def list_compare(list1, list2):
    """
    checks whether given iterables are equal, used for np.array/tuple coordinates
    """
    comparison = list1 == list2
    return comparison.all()

def list_in(list, list_of_lists):
    """
    checks whether iterables is in list of iterables, used for np.array/tuple coordinates
    """
    for other_list in list_of_lists:
        if list_compare(list, other_list):
            return True
    return False

def is_valid(start, adjustment, used_lines, forbidden_gates, grid):
    line = {tuple(start), tuple(start + adjustment)}
    if not line in used_lines and not list_in(start + adjustment, forbidden_gates) and check_max_value(start + adjustment, grid):
        return True
    return False

def is_almost_valid(start, adjustment, forbidden_gates, grid):
    if not list_in(start + adjustment, forbidden_gates) and check_max_value(start + adjustment, grid):
        return True
    return False