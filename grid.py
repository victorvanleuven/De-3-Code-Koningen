class Grid():
    def __init__(self, gate_dict):
        # input moet dict zijn, met gate_nr = key en coordinaten van gate in tuple
        self.gate_dict = gate_dict
        # n: x, y

    def get_coord(self, gate):
        return self.gate_dict[gate]