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
