class Netlist():
    def __init__(self, connections):
        # lijst van tuples, chips die met elkaar geconnect zijn
        self.connections = connections

    # input = gate, output = alle gates waarmee input gate een connectie heeft
    def get_connections(self, gate):
        pass