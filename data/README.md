## `time_memory_usage.csv`
Data on the time, memory, and disk space usage of Blendplot and Blender in plotting a dataset using different amounts of data points.

In this case, the test used data from the [HYG 3.0 database](http://astronexus.com/node/34) and plotted numbers of points between 1 and 100,001 at regular intervals of 1,000.

The version of Blendplot used was at commit `4e49f0738c69e2bb9346ab12dd88ebda81139e80`. The version of Blender used was `2.78c`. The operating system used was Ubuntu Linux 16.04.2 LTS.

* `points` - The number of points plotted in the scatter plot.
* `t_obj` - The time in seconds it took from Blendplot to generate the `.obj` plot.
* `t_import` - The time in seconds it took Blender to import the `.obj` file.
* `t_save` - The time in seconds it took Blender to save the `.blend` file resulting from importing the plot.
* `t_total` - The sum of the previous time measures.
* `memory` - The maximum amount of RAM used in GB by Blender during the importing of the `.obj` file.
* `size_obj` - The file size in MB of the `.obj` file created by Blendplot.
* `size_blend` - The file size in MB of the `.blend` file created by Blender.
* `size_total` - The sum of the previous two size measures.
