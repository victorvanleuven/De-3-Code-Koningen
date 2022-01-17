"""
first algorithm based on the baseline, but avoiding overlap and even intersections by utilising upper layers
"""

import numpy as np

def list_compare(list1, list2):
    comparison = list1 == list2
    return comparison.all()

def list_in(list, list_of_lists):
    for other_list in list_of_lists:
        if list_compare(list, other_list):
            return True
    return False

def greedy_move(start, destination, invalid_steps):
    start = np.array(start)
    destination = np.array(destination)

    for direction in range(3):
        adjustment = np.array((0,0,0))
        if start[direction] > destination[direction]:
            adjustment[direction] -= 1
            if not list_in(start + adjustment, invalid_steps):
                return adjustment
        elif start[direction] < destination[direction]:
            adjustment[direction] += 1
            if not list_in(start + adjustment, invalid_steps):
                return adjustment

    # if we can't move more towards our destination, try to go up
    adjustment = np.array((0,0,1))
    if not list_in(start + adjustment, invalid_steps):
        return adjustment

    return np.array((0,0,0))

def actualsolvecircuit(netlist, grid):
    netlist = netlist.connections
    gates = grid.gate_dict
    gate_coords = list(gates.values())
    connection_path_dict = {}
    invalid_positions= []

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
        still_going = True

        while still_going:
            adjustment = greedy_move(step, coords_gate_b, invalid_positions)

            comparison = adjustment == np.array((0,0,0))
            if comparison.all() == True:
                print ("comparison")
                print(comparison)
                print("position")
                print("step + adjustment")
                print(step+adjustment)
                print("") 
                still_going = False

            step = step + adjustment
            if not list_in(step, gate_coords): 
                invalid_positions.append(step)
            path.append(tuple(step))
        
        connection_path_dict[connection] = path
    
    return connection_path_dict


def oud(netlist, grid):
    
    connection_path_dict = {}
    # dictionary which tells for every point in the grid which neighbours we cannot travel to
    invalid_steps = []

    # get all gates coordinates
    gate_coords_dict = grid.gate_dict
    gate_coords = list(gate_coords_dict.values())

    for connection in netlist.connections:
        # get gates and their coordinates
        gate_a = connection[0]
        gate_b = connection[1]

        # retrieve gate coordinates as tuples
        coords_gate_a = gate_coords_dict[gate_a]
        coords_gate_b = gate_coords_dict[gate_b]
        
        # start at gate_a and build a path from gate_a to gate_b
        step = coords_gate_a
        path = [step]

        # abort after 200 tries
        tries = 0

        # strive for shortest path, but avoid all intersections
        while step != coords_gate_b and tries < 1000:
            tries += 1
            counter = 0
            # for every coordinate, try to do a step in b's direction
            for coord in range(3):
                if step[coord] < coords_gate_b[coord]:
                    possible_step = np.array(step)
                    possible_step[coord] += 1
                    possible_step = tuple(possible_step)
                elif step[coord] > coords_gate_b[coord]:
                    possible_step = np.array(step)
                    possible_step[coord] -= 1
                    possible_step = tuple(possible_step)
                else:
                    # if we already are at the right coordinate in this direction, go to the next coordinate
                    if coord != 2:
                        continue
                    # we can move in z direction if there's no possible step
                    possible_step = np.array(step)
                    possible_step[coord] += 1
                    possible_step = tuple(possible_step)
                
                # check if step was already made, if so go to next coordinate, else perform step
                if possible_step not in invalid_steps:
                    if possible_step not in gate_coords:
                        invalid_steps.append(possible_step)
                    step = possible_step
                    path.append(step)

        connection_path_dict[connection] = path
    
    return connection_path_dict