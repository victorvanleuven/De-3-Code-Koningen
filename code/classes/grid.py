import csv


# maakt van 2d coordinaten (tuple) 3d coordinaten door een 0 toe te voegen.
def project_three_d(coord):
    if len(coord) == 2:
        coord += (0,)
    return coord


class Grid():
    def __init__(self, source_file):
        # input moet dict zijn, met gate_nr = key en coordinaten van gate in tuple
        self.gate_dict = self.load_grid(source_file)
        # n: x, y

    def get_coord(self, gate):
        return self.gate_dict[gate]

    def load_grid(self, filename_grid):
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
