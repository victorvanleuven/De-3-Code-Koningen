import matplotlib.pyplot as plt
from code.classes.grid import Grid
from code.visualisation.load_output import load_output


def visualize_grid(filename_visualization, filename_grid, filename_solution):

    grid = Grid(filename_grid)
    gates = grid.gate_dict
    for key in gates.keys():
        x = gates[key][0]
        y = gates[key][1]

    paths = load_output(filename_solution)
    
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
        
        if len(gates.keys()) < 20:
            for key in gates.keys():
                x = gates[key][0]
                y = gates[key][1]
                ax.plot(x,y,0,".")
                ax.text(x,y,0, key)
        ax.plot(x_list, y_list, z_list)

    ax.set_zticks(range(8))
    plt.savefig(filename_visualization)       

