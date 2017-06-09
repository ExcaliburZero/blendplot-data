import itertools
import numpy as np
import sys
import time

import sys_utilities

def main():
    """
    $ python3 render_info.py ~/Datasets/hyg/hygdata_v3.csv
    """
    data_file = sys.argv[1]
    model_types = ["obj", "dupliverts"]
    start = 1
    end = 100002
    interval = 5000
    points = np.arange(start, end, interval)

    print("type,points,t_all,max_memory,avg_cpu,t_plot,t_render")

    for (mt, p) in itertools.product(model_types, points):
        measures = get_measures(mt, data_file, p)

        print("%s,%d,%s" % (mt, p, ",".join(map(str,measures))))

def get_measures(model_type, data_file, num_points):
    start = time.time()
    (max_memory, avg_cpu, t_plot, t_render) = load_model_render(model_type, data_file, num_points)
    end = time.time()

    t_all = end - start

    return t_all, max_memory, avg_cpu, t_plot, t_render

def load_model_render(model_type, data_file, num_points):
    info = None

    info_gatherers = [
                sys_utilities.MemoryRecorder(),
                sys_utilities.CPURecorder()
            ]

    info = load_render(model_type, data_file, info_gatherers, num_points)

    return info

def load_render(model_type, data_file, info_gatherers, num_points):
    script = "render_blend.py"
    info_file = ".render_info.txt"

    args = [info_file, data_file, str(num_points), model_type]

    info = sys_utilities.fully_run_blender_script(script, info_gatherers = info_gatherers, args = args)

    more_info = read_file(info_file).split("\n")

    return max(info[0]), np.mean(info[1]), more_info[0], more_info[1]

def read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()

if __name__ == "__main__":
    main()
