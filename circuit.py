class Net():
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
        intersections = 1

        return wire_length + 300 * intersections

    def intersections(self):
        intersections = 0
        nodes_taken = []
        for connection in self.connection_wire_dict.keys():
            # we don't count paths with the same end or beginning as intersections
            path = (self.connection_wire_dict[connection])[1:-1]
            for node in path:
                if node in nodes_taken:
                    intersections += 1
                else:
                    nodes_taken.append(node)

        return intersections

