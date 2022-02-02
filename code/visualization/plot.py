"""
this is an example of how we plotted our data, we used this to make a histogram of the costs of our baseline algorithm
"""

import pandas
import matplotlib.pyplot as plt

# choose which csv file to use
filename_output = "/Users/pieterout/programmeertheorie/De-3-Code-Koningen/test/batchruns/netlist_4_gr_hill_15.csv"

dataframe = pandas.read_csv(filename_output)

dataframe = dataframe[dataframe.connections == 30]

cost_list = dataframe["cost"]

cost_list.plot.kde(bw_method=0.5)

plt.xlim([0, 50000])
plt.xlabel("Cost")

plt.hist(cost_list, bins=10, density=True, histtype="bar", rwidth=0.75)

plt.savefig("first_plot.png")
