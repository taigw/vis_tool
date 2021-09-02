
import csv
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_forest_plot(input_csv, output_png):
    items  = pd.read_csv(input_csv)
    names = list(items.iloc[:, 0])
    pvalue= list(items.iloc[:, 1])
    oddratio = list(items.iloc[:, 2])
    lower = list(items.iloc[:, 3])
    upper = list(items.iloc[:, 4])
    weight= list(items.iloc[:, 5])
    lab_n = len(names)
    labels = ["{0:} (pvalue = {1:})".format(names[n], pvalue[n]) \
            for n in range(lab_n)]

    fig, ax = plt.subplots(1, 1, figsize = (7.5, 2.5))
    secax_lab = []
    for n in range(lab_n):
        y = lab_n - n 
        x0 = lower[n]
        x1 = upper[n]
        xc = oddratio[n]
        plt.plot([x0, x1], [y, y], color = 'b')
        plt.plot(xc, y, 'd', color='b')

        ci = "({0:.2f}, {1:.2f})".format(x0, x1)
        ci = ci + " "*(15- len(ci))
        temp_lab = "{0:.2f}  {1:} {2:.2f}".format(xc, ci, weight[n])
        secax_lab.append(temp_lab)
    xmin = np.asarray(lower).min()
    xmax = math.ceil(np.asarray(upper).max())
    plt.xlim(0.01, xmax)
    plt.xticks([0.01, xmax], [0.01, "{0:}".format(xmax)])
    plt.yticks(range(1, lab_n + 1), reversed(labels))
    plt.ylim(0, lab_n + 0.5)
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='y', **{'length':0})

    secax_y = ax.secondary_yaxis('right')
    secax_y.set_yticks(range(1, lab_n + 1))
    secax_y.set_yticklabels(reversed(secax_lab))
    secax_y.tick_params(axis='y', **{'length':0})
    plt.text(xmax, lab_n + 0.5, "  OR")
    plt.text(xmax + 3, lab_n + 0.5, "  95% CI")
    plt.text(xmax + 8.5, lab_n + 0.5, "  Weight")
    plt.plot([1, 1], [0, lab_n + 0.5], color = 'black', linewidth=1)
    plt.subplots_adjust(left=0.28, right=0.72, top=0.8, bottom=0.1)
    plt.savefig(output_png)
    plt.show()

input_csv = "./data/forest_plot.csv"
output_png= "./data/forest_plot.png"
create_forest_plot(input_csv, output_png)
