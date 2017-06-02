import bpy
import subprocess
import sys
import _thread
import time

def main():
    obj_file = "tmp_time_memory_usage.obj"
    blend_file = "tmp_time_memory_usage.blend"
    memory_file = "tmp_memory.txt"
    import_time_file = "tmp_t_import.txt"
    save_time_file = "tmp_t_save.txt"

    mem_watch = MemoryWatcher()
    mem_watch.start()

    start = time.time()
    import_file(obj_file)
    end = time.time()
    t_blend = end - start

    max_ram = 8.0 # in GB
    mem_percent = mem_watch.poll()
    memory = (mem_percent / 100.0) * max_ram

    start = time.time()
    save_file(blend_file)
    end = time.time()
    t_save = end - start

    write_to_file(memory_file, str(memory))
    write_to_file(import_time_file, str(t_blend))
    write_to_file(save_time_file, str(t_save))

    sys.exit(0)

def import_file(obj_file):
    bpy.ops.import_scene.obj(filepath=obj_file)

def save_file(blend_file):
    bpy.ops.wm.save_as_mainfile(filepath=blend_file)

def write_to_file(file_name, data):
    with open(file_name, "w") as f:
        f.write(data)

class MemoryWatcher(object):

    max_memory = None
    cont = None

    def __init__(self):
        self.max_memory = 0.0
        self.cont = True

    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        while self.cont:
            new_mem = get_memory()
            if new_mem > self.max_memory:
                self.max_memory = new_mem
            time.sleep(0.01)

    def poll(self):
        self.cont = False
        return self.max_memory

def get_memory():
    command = "ps aux | grep blender | head -n 1 | awk '{print $4}'"
    memory = float(subprocess.check_output(command, shell=True))

    return memory

if __name__ == "__main__":
    main()
