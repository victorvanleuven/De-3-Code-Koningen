import csv

class Netlist():
    def __init__(self, source_file):
        # lijst van tuples, chips die met elkaar geconnect zijn
        self.connections = self.load_netlist(source_file)

    # input = gate, output = alle gates waarmee input gate een connectie heeft
    def get_connections(self, gate):
        pass

    def load_netlist(self, filename_netlist):
        netlist = []

        with open(filename_netlist) as file:
            csvreader = csv.reader(file, delimiter=',')

            # skipping headers of csv
            next(csvreader)

            for row in csvreader:
                row = tuple(map(int, row))
                netlist.append(row)
        return netlist
