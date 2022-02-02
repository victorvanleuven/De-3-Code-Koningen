class Circuit():
    def __init__(self, connection_path_dict):
        # tuple als key, met lijst van tuples(coords)
        self.connection_path_dict = connection_path_dict

    def cost(self):
        """
        calculates the cost of a solution
        """
        wire_length = 0
        for key in self.connection_path_dict:
            connection_length = len(self.connection_path_dict[key]) - 1
            wire_length += connection_length
        
        return wire_length + 300 * self.intersections()

    def intersections(self):
        """
        counts all intersections in a solution
        """
        paths_used = self.connection_path_dict.values()
        nodes_used = [item for sublist in paths_used for item in sublist]
        
        # calculate total intersections
        intersections = len(nodes_used) - len(set(nodes_used))
        connections = self.connection_path_dict.keys()

        # intersections in gates don't count, substract these
        gates = ()
        for connection in connections:
            gates += tuple(connection)

        gate_intersections = len(gates) - len(set(gates))

        return intersections - gate_intersections

