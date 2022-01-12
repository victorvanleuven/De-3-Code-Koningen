class Circuit():
    def __init__(self, connection_wire_dict):
        # tuple als key, met lijst van tuples(coords)
        self.connection_wire_dict = connection_wire_dict
        pass

    def cost(self):
        wire_length = 0
        for key in self.connection_wire_dict:
            connection_length = len(self.connection_wire_dict[key]) - 1
            wire_length += connection_length
        
        # alle lijsten samenvoegen, aantal duplicates tellen en dat is aantal intersections met union
        # verschil lengte oorspronkelijke lijst en lengte set = aantal intersections
        # kan sneller met intersect maar werkt misschien niet door verwijderen van intersections als er meer dan 2 samen komen

        return wire_length + 300 * self.intersections()

    def intersections(self):
        # every duplicate node is an intersection
        nodes_used = self.connection_wire_dict.values()
        intersections = len(nodes_used) - len(set(nodes_used))

        # intersections in gates don't count, substract these
        connections = self.connection_wire_dict.keys()
        # make tuple containing all endpoints, including duplicates
        endpoints = ()
        for connection in connections:
            endpoints += connection

        endpoint_intersections = len(endpoints) - len(set(endpoints))

        return intersections - endpoint_intersections

