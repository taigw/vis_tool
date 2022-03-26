# vis_tool
Python scripts to visualize exeprimental results for image computing researches

# Functions:
1, Visualize a segmentation result compared with the ground truth. 
```bash 
python show_segmentation_contour.py
```
<img src="./data/contour.png" width ="256">

In this example, the ground truth is shown in yellow color and the segmentation is shown with green color.


2, Use boxplot to compare the performance of different methods on a set of data.
```bash 
python show_boxplot.py
```
<img src="./data/performance_boxplot.png" width="256">

3, Use seaborn to show boxplot.
```bash
python show_boxplot_seaborn.py
```
<img src="./data/seaborn_boxplot.png">

4, Fuse a heatmap with an image
```bash 
python show_fused_heatmap.py
```
<img src="./data/img_vs_example.png">

5, Show forest plot of logitic regression
```
python show_forest_plot.py
```
<img src="./data/forest_plot.png">