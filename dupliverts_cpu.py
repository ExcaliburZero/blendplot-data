import pyautogui as gui
import subprocess
import sys
import time
import _thread

def main():
    import_mode = "dupliverts"

    if import_mode == "dupliverts":
        load_dupliverts()
    else:
        load_obj()

    t_drag, mem_drag, cpu_drag = drag_model()

    print("Memory: %s" % mem_drag)
    print("\n".join(map(str, cpu_drag)))

def drag_model():
    cpu_recorder = CPURecorder()
    memory_watcher = MemoryWatcher()
    cpu_recorder.start()
    memory_watcher.start()

    start = time.time()
    drag()
    end = time.time()

    time.sleep(8.0)

    cpu_drag = cpu_recorder.poll()
    mem_drag = memory_watcher.poll()
    
    t_drag = end - start

    return t_drag, mem_drag, cpu_drag

def drag():
    alt = "alt"
    x = 4600
    y = 500
    drag_x = 200
    gui.moveTo(x, y)
    gui.click()
    time.sleep(0.01)
    gui.keyDown(alt)
    gui.dragRel(drag_x, 0, 1, button="left")
    gui.keyUp(alt)

def load_dupliverts():
    dupliverts_script = "plot_dupliverts.py"
    command = ["blender", "--python", dupliverts_script]

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    time.sleep(10)
    print("Loaded dupliverts")

def load_obj():
    command = ["blender", "/home/chris/Blender/hyg.blend"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    time.sleep(10)
    print("Loaded obj")

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

class CPURecorder(object):

    cpu_curve = None
    cont = None

    def __init__(self):
        self.cpu_curve = []
        self.cont = True

    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        while self.cont:
            new_cpu = get_cpu()
            self.cpu_curve.append(new_cpu)
            time.sleep(0.01)

    def poll(self):
        self.cont = False
        return self.cpu_curve

def get_memory():
    command = "ps aux | grep blender | head -n 1 | awk '{print $4}'"
    memory = float(subprocess.check_output(command, shell=True))

    return memory

def get_cpu():
    command = "ps aux  | awk 'BEGIN { sum = 0 }  { sum += $3 }; END { print sum }'"
    cpu = float(subprocess.check_output(command, shell=True)) / 4.0

    return cpu

if __name__ == "__main__":
    main()
