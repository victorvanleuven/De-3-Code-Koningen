import matplotlib.pyplot as plt
from code.classes.grid import Grid
from code.visualisation.load_output import load_output


def visualize_grid(filename_visualization, filename_grid, filename_solution):

    grid = Grid(filename_grid)
    gates = grid.gate_dict
    for key in gates.keys():
        x = gates[key][0]
        y = gates[key][1]
    #     plt.plot(x, y, 0,".")
    #     plt.annotate(key, (x,y))

    # plt.grid(visible=True, which='major', axis="both")
    # plt.savefig(filename_visualization)

    paths = load_output(filename_solution)
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
        
        for key in gates.keys():
            x = gates[key][0]
            y = gates[key][1]
            ax.plot(x,y,0,".")
            ax.text(x,y,0, key)
        ax.plot(x_list, y_list, z_list)

        # # 2d plot als er niet meerdere lagen zijn
        # plt.plot(x_list, y_list)

    ax.set_zticks(range(8))
    plt.savefig(filename_visualization)       

