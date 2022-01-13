import matplotlib.pyplot as plt
from loader import *


output_file_name = "grid.png"
filename_grid = "data/gates&netlists/chip_0/print_0.csv"
filename_netlist = "data/gates&netlists/chip_0/netlist_1.csv"
filename_output = "example/output.csv"

def print_grid():

    gates = load_grid(filename_grid)
    for key in gates.keys():
        x = gates[key][0]
        y = gates[key][1]
        plt.plot(x, y, ".")
        plt.annotate(key, (x,y))

    plt.grid(visible=True, which='major', axis="both")
    plt.savefig(output_file_name)

    paths = load_output(filename_output)
    # print(paths)
    
    ax = plt.figure().add_subplot(projection='3d')
    for path in paths:
        x_list = []
        y_list = []
        z_list = []
        for coord in path:
            x_list.append(coord[0])
            y_list.append(coord[1])
            z_list.append(coord[2])
        
        # 3d plot voor als er meerdere lagen zijn
        
        ax.plot(x_list, y_list, z_list)

        # # 2d plot als er niet meerdere lagen zijn
        # plt.plot(x_list, y_list)

    
    plt.savefig(output_file_name)       

print_grid()
