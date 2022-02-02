import csv


def project_three_d(coord):
    """
    projects 2d coordinates into 3d coordinates in the z=0 plane
    """
    if len(coord) == 2:
        coord += (0,)
    return coord

class Grid():
    """
    class of a grid holding gates
    """
    def __init__(self, source_file):
        self.gate_dict = self.load_grid(source_file)

    def load_grid(self, filename_grid):
        """
        loads csv file of grid into dictionary (connections as keys and paths as values)
        """
        gate_coord_dict = {}

        with open(filename_grid) as file:
            csvreader = csv.reader(file, delimiter=',')

            # skips headers of csv
            next(csvreader)

            for row in csvreader:
                gate = int(row[0])
                coordinates = tuple(row[1:])
                coordinates_int = tuple(map(int, coordinates))
                gate_coord_dict[gate] = project_three_d(coordinates_int)
        
        return gate_coord_dict

    def get_maxmin_xy(self):
        """
        returns dictionary of maximum and minimum x and y values
        """
        x_values = []
        y_values = []

        for coordinate in self.gate_dict.values():
            x_values.append(coordinate[0])
            y_values.append(coordinate[1])
        
        max_x = max(x_values)
        min_x = min(x_values)
        max_y = max(y_values)
        min_y = min(y_values)

        return {"max_x": max_x, "min_x": min_x, "max_y": max_y, "min_y": min_y}
            
            

