import csv

class Netlist():
    """
    class of connected gates
    """
    def __init__(self, source_file):
        self.connections = self.load_netlist(source_file)

    def load_netlist(self, filename_netlist):
        """
        retrieves list of all connections from a netlist csv
        """
        netlist = []

        with open(filename_netlist) as file:
            csvreader = csv.reader(file, delimiter=',')

            # skipping headers of csv
            next(csvreader)

            for row in csvreader:
                row = tuple(map(int, row))
                netlist.append(row)
        return netlist
