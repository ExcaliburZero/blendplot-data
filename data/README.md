## `cpu_*.txt`
Recordings of the total CPU usage over time while a model creating using obj import and dupliverts plotting respectively were dragged around in Blender.

In this case, the test used data from the [HYG 3.0 database](http://astronexus.com/node/34) and the entire dataset was used for both tests, for a total of 119,614 points.

The version of Blender used was `2.78c`. The operating system used was Ubuntu Linux 16.04.2 LTS.

Each line in the file represents the total system CPU usage (%) at an interval. The intervals are roughly regular with approximately 0.01 seconds in between readings.

The CPU measure also includes the CPU usage of other processes running on the system at the time, but the tests were run with few other applications open so the measures across the two tests are reasonably comparable.

## `obj_v_dupliverts_memory.csv`
Data on the max memory usage when dragging obj imported and dupliverts plotted models in Blender.

In this case, the test used data from the [HYG 3.0 database](http://astronexus.com/node/34) and the entire dataset was used for both tests, for a total of 119,614 points.

The version of Blender used was `2.78c`. The operating system used was Ubuntu Linux 16.04.2 LTS.

* `type` - The tye of scatter plot used in the test.
* `memory` - The maximum amount of RAM used in GB by Blender during the model dragging.

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
