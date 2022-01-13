import numpy as np

def solvecircuit(netlist, gate_coords):
    # eerste versie, lost op met zo kort mogelijke routes maar niet perse kloppend (overlap)
    connection_path_dict = {}

    for connection in netlist:
        gate_a = connection[0]
        gate_b = connection[1]

        coords_gate_a = gate_coords[gate_a]
        coords_gate_b = gate_coords[gate_b]
        
        path = []
        step = np.array(coords_gate_a)
        path.append(tuple(step))
        for coord in range(3):
            while step[coord] != coords_gate_b[coord]:
                if step[coord] > coords_gate_b[coord]:
                    step[coord] -= 1
                if step[coord] < coords_gate_b[coord]:
                    step[coord] += 1
                path.append(tuple(step))

        connection_path_dict[connection] = path
    
    return connection_path_dict