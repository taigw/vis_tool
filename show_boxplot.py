import numpy as np
from numpy import loadtxt
import matplotlib.pyplot as plt

def show_performance():
    method_names    = ['Method1','Method2','Method3']
    data_file_names = ['data/performance_method1.txt',
                       'data/performance_method2.txt',
                       'data/performance_method3.txt']
    output_name     =  'data/performance_boxplot.pdf'
    Data = [np.array(loadtxt(item)) for item in data_file_names]

    fig=plt.figure(figsize=(2.5, 2.5))
    x=[1,2,3]
    plt.boxplot(Data)
    ylabel = "Performance"
    plt.ylim(0, 350)
    plt.ylabel(ylabel)
    plt.xticks(x, method_names,rotation=30,ha='right')
    plt.subplots_adjust(left=0.3, right=0.8, top=0.95, bottom=0.25)
    plt.show()
    fig.savefig(output_name)

show_performance()
