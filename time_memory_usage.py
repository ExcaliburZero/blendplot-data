import numpy as np
import os
import subprocess
import sys
import time

def main():
    """
    $ python3 time_memory_usage.py ~/Datasets/hyg/hygdata_v3.csv x y z > data/time_memory_usage.csv
    """
    input_file = sys.argv[1]
    obj_file = "tmp_time_memory_usage.obj"
    blend_file = "tmp_time_memory_usage.blend"
    import_script = "import_model.py"
    memory_file = "tmp_memory.txt"
    import_time_file = "tmp_t_import.txt"
    save_time_file = "tmp_t_save.txt"
    x = sys.argv[2]
    y = sys.argv[3]
    z = sys.argv[4]

    start = 1
    end = 100002
    interval = 1000
    values = np.arange(start, end, interval)

    print("points,t_obj,t_import,t_save,t_total,memory,size_obj,size_blend,size_total")
    for v in values:
        (t_obj, t_import, t_save, memory, size_obj, size_blend) = plot_info(v, input_file, obj_file,
                blend_file, import_script, memory_file, import_time_file,
                save_time_file, x, y, z)
        t_total = t_obj + t_import + t_save
        size_total = size_obj + size_blend
        print("%d,%f,%f,%f,%f,%f,%f,%f,%f" % (v, t_obj, t_import, t_save, t_total, memory, size_obj, size_blend, size_total))

def plot_info(num_values, input_file, obj_file, blend_file, import_script,
        memory_file, import_time_file, save_time_file, x, y, z):
    t_obj = create_obj(input_file, obj_file, num_values, x, y, z)

    (t_import, t_save, memory) = blender_import(obj_file, import_script, memory_file, import_time_file, save_time_file)

    size_obj = get_file_size(obj_file)
    size_blend = get_file_size(blend_file)

    return (t_obj, t_import, t_save, memory, size_obj, size_blend)

def get_file_size(file_name):
    size_bytes = os.path.getsize(file_name)
    size_mb = size_bytes / 1000000.0

    return size_mb

def create_obj(input_file, obj_file, num_values, x, y, z):
    command = ["blendplot", input_file, obj_file, x, y, z, "-r", str(num_values)]

    start = time.time()
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    process.wait()
    end = time.time()

    return end - start

def blender_import(obj_file, import_script, memory_file, import_time_file, save_time_file):
    command = ["blender", "--background", "--python", import_script]

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    process.wait()

    memory = float(read_file(memory_file))
    t_import = float(read_file(import_time_file))
    t_save = float(read_file(save_time_file))

    return (t_import, t_save, memory)

def read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()

if __name__ == "__main__":
    main()
