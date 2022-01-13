import argparse
import loader
import solve_circuit
from circuit import Circuit
import csv

def main(grid, netlist, output, visualisation):
    netlist = loader.load_netlist(netlist)
    grid = loader.load_grid(grid)

    solved = solve_circuit.solvecircuit(netlist, grid)
    print(solved)
    headers = ["net", "wires"]
    

    circuit = Circuit(solved)
    print(circuit)

      
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "Generates connections between gates in a chip with the lowest cost possible.")

    # Adding arguments
    parser.add_argument("print", help = "print file (csv)")
    parser.add_argument("netlist", help = "netlist file (csv)")
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("visualisation", help = "visualization (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.print, args.netlist, args.output, args.visualisation)