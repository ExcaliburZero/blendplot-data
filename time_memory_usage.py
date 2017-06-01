import numpy as np
import os
import subprocess
import sys
import time

def main():
    input_file = sys.argv[1]
    obj_file = "tmp_time_memory_usage.obj"
    import_script = "import_model.py"
    memory_file = "tmp_memory.txt"
    x = sys.argv[2]
    y = sys.argv[3]
    z = sys.argv[4]

    start = 1
    end = 100002
    interval = 1000
    values = np.arange(start, end, interval)

    print("points,t_obj,t_blend,memory")
    for v in values:
        (t_obj, t_blend, memory) = plot_info(v, input_file, obj_file, import_script, memory_file, x, y, z)
        print("%d,%f,%f,%f" % (v, t_obj, t_blend, memory))

def plot_info(num_values, input_file, obj_file, import_script, memory_file, x, y, z):
    t_obj = create_obj(input_file, obj_file, num_values, x, y, z)

    (t_plot, memory) = blender_import(obj_file, import_script, memory_file)

    return (t_obj, t_plot, memory)

def create_obj(input_file, obj_file, num_values, x, y, z):
    command = ["blendplot", input_file, obj_file, x, y, z, "-r", str(num_values)]

    start = time.time()
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    process.wait()
    end = time.time()

    return end - start

def blender_import(obj_file, import_script, memory_file):
    command = ["blender", "--background", "--python", import_script]

    start = time.time()
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    process.wait()
    end = time.time()

    memory = float(read_file(memory_file))

    return (end - start, memory)

def read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()

if __name__ == "__main__":
    main()
