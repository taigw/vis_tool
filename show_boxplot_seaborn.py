import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.weight"] = 'normal'
 
expr = 2
csv_file = "data/seaborn_boxplot.csv"
savename = "data/seaborn_boxplot.pdf"
metrics = ['Metric 1', 'Metric 2', "Metric 3"]
data = pd.read_csv(csv_file)

flierprops = dict(marker = '.', markerfacecolor = '1.0', markersize = 1,  linestyle = 'none')
sns.set_context("paper", font_scale = 0.6)
fig = plt.figure(figsize = (7.5, 1.35), dpi = 300)

plt.subplot(1,3,1)
#sns.set(style = "whitegrid")
ax = sns.boxplot(x = "Group", y = metrics[0], hue = "Method", linewidth=.5,
      data = data, flierprops = flierprops)
plt.ylabel(metrics[0])
plt.xlabel('')
plt.ylim(0.2, 1)
ax.get_legend().remove()

plt.subplot(1,3,2)
#sns.set(style = "whitegrid")
ax = sns.boxplot(x = "Group", y = metrics[1], hue = "Method",linewidth=.5,
      data = data, flierprops = flierprops)
plt.ylabel(metrics[1])
plt.xlabel('')
plt.ylim(0, 1)
plt.legend().remove()

plt.subplot(1,3,3)
#sns.set(style = "whitegrid")
ax = sns.boxplot(x = "Group", y =  metrics[2], hue = "Method", linewidth=.5,
      data = data, flierprops = flierprops)    
plt.ylabel(metrics[2])
plt.xlabel('')
plt.ylim(0, 120 )

plt.legend(bbox_to_anchor=(1.1, 1), loc=2, borderaxespad=0.)
plt.subplots_adjust(left = 0.075, right = 0.8, bottom = 0.2, wspace = 0.55)

plt.show()
fig.savefig(savename)