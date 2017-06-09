import time
import _thread
import subprocess

def start_blender_script(script_name, background = True, args = []):
    command = ["blender"]

    if background:
        command.append("--background")
    
    command.append("--python")
    command.append(script_name)

    if len(args) > 0:
        command.append("--")
        for a in args:
            command.append(a)

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    return process

def fully_run_blender_script(script_name, background = True, info_gatherers = [], args = []):
    for g in info_gatherers:
        g.start()

    process = start_blender_script(script_name, background, args)
    process.wait()

    return [g.poll() for g in info_gatherers]

class Watcher(object):

    measure_func = None
    max_measure = None
    cont = None
    interval = None

    def __init__(self, measure_func, min_measure, interval):
        self.measure_func = measure_func
        self.max_measure = min_measure
        self.interval = interval
        self.cont = True

    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        while self.cont:
            self.update_measure()
            time.sleep(self.interval)

    def update_measure(self):
        new_measure = self.measure_func()
        if new_measure > self.max_measure:
            self.max_measure = new_measure

    def poll(self):
        self.cont = False
        return self.max_measure

class MemoryWatcher(Watcher):

    def __init__(self):
        measure_func = get_memory
        min_measure = 0.0
        interval = 0.01
        Watcher.__init__(self, measure_func, min_measure, interval)

class Recorder(object):

    measure_func = None
    curve = None
    cont = None

    def __init__(self, measure_func, interval):
        self.measure_func = measure_func
        self.interval = interval
        self.curve = []
        self.cont = True

    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        while self.cont:
            self.add_measure()
            time.sleep(self.interval)

    def add_measure(self):
        new_measure = self.measure_func()
        self.curve.append(new_measure)

    def poll(self):
        self.cont = False
        return self.curve

class CPURecorder(Recorder):

    def __init__(self):
        measure_func = get_cpu
        interval = 0.01
        Recorder.__init__(self, measure_func, interval)

class MemoryRecorder(Recorder):

    def __init__(self):
        measure_func = get_memory
        interval = 0.01
        Recorder.__init__(self, measure_func, interval)

def get_memory():
    command = "ps aux | grep blender | head -n 1 | awk '{print $4}'"
    memory = float(subprocess.check_output(command, shell=True))

    return memory

def get_cpu():
    command = "ps aux  | awk 'BEGIN { sum = 0 }  { sum += $3 }; END { print sum }'"
    cpu = float(subprocess.check_output(command, shell=True)) / 4.0

    return cpu
