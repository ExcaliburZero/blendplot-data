import bpy
import pandas as pd
import os
import sys
import time

def get_args():
    args_start = sys.argv.index("--")
    args = sys.argv[args_start + 1:]
    
    return args

def main():
    args = get_args()
    
    info_file = args[0]
    data_file = args[1]
    num_points = int(args[2])
    model_type = args[3]

    setup_scene()
    
    t_load = load_model(data_file, num_points, model_type)
    
    t_render = render_image()
    
    info = "\n".join(map(str,[t_load, t_render]))
    write_to_file(info_file, info)

def setup_scene():
    try:
        # Delete default cube
        bpy.context.scene.objects["Cube"]
        bpy.ops.object.delete()
    except KeyError:
        # It is okay if the cube is not there
        pass

    camera = bpy.context.scene.objects["Camera"]

    x = 0
    y = -41
    z = 0

    xr = 90 / 57.295777919
    yr = 0
    zr = 0

    camera.location = (x, y, z)
    camera.rotation_euler = (xr, yr, zr)
    
    bpy.data.worlds["World"].light_settings.use_ambient_occlusion = True
    
def load_model(data_file, num_points, model_type):
    if model_type == "obj":
        return load_model_obj(data_file, num_points)
    else:
        return load_model_dupliverts(data_file, num_points)
    
def load_model_obj(data_file, num_points):
    tmp_obj = "/tmp/model.obj"
    
    start = time.time()
    command = "blendplot %s %s x y z -r %d --scale-function none --spacing 0.0001 --point-size 0.05" % (data_file, tmp_obj, num_points)
    os.system(command)
    
    bpy.ops.import_scene.obj(filepath=tmp_obj)
    end = time.time()
    
    return end - start
    
def load_model_dupliverts(data_file, num_points):
    tmp_obj = "/tmp/model.obj"
    
    data = pd.read_csv(data_file, nrows = num_points)
    start = time.time()
    plot_dupliverts(data, "x", "y", "z", 0.0001, 0.05, "1", "2", "3", bpy.ops.mesh.primitive_cube_add)
    end = time.time()
    
    return end - start

def render_image():
    start = time.time()
    #fp = "/tmp/" + (str(int(start)))
    #bpy.data.scenes['Scene'].render.filepath = fp + ".png"
    #bpy.ops.render.render(write_still=True)
    bpy.ops.render.render()
    #print(bpy.context.scene.render.filepath)
    end = time.time()

    #bpy.ops.wm.save_as_mainfile(filepath=fp + ".blend")
    
    t_render = end - start
    
    return t_render

def write_to_file(file_name, data):
    with open(file_name, "w") as f:
        f.write(data)
        
def plot_dupliverts(data, x_col, y_col, z_col, scaling, point_size, mesh_name, plot_name, ref_point_name, create_ref_point):
    """
    Plots the given data as a scatter plot using dupliverts.
    """
    verts = get_verts(data, x_col, y_col, z_col, scaling)
    plot_verts(verts, point_size, mesh_name, plot_name, ref_point_name, create_ref_point)

def get_verts(data, x_col, y_col, z_col, scaling):
    """
    Get the (x,y,z) verticies from the given data frame using the given columns
    and point range scaling.
    """
    def get_xyz(row):
        x = row[x_col] * scaling
        z = row[y_col] * scaling #SWAPPED
        y = row[z_col] * scaling * -1.0 #SWAPPED & NEGATED
        return x, y, z

    verts = data.apply(get_xyz, axis=1)
    return verts

def plot_verts(verts, point_size, mesh_name, plot_name, ref_point_name, create_ref_point):
    """
    Plot the given (x,y,z) scatter plot verticies using the given information.
    """
    plot_obj = create_plot_obj(verts, mesh_name, plot_name)
    ref_point = create_reference_point_obj(point_size, ref_point_name, create_ref_point)

    setup_dupliverts(plot_obj, ref_point)

def create_plot_obj(verts, mesh_name, plot_name):
    """
    Creates the plot object using the given vertex positions.
    """
    mesh = bpy.data.meshes.new(mesh_name)
    plot_obj = bpy.data.objects.new(plot_name, mesh)

    scene = bpy.context.scene
    scene.objects.link(plot_obj)

    mesh.from_pydata(verts, [], [])
    mesh.update()

    return plot_obj

def create_reference_point_obj(point_size, ref_point_name, create_ref_point):
    """
    Creates the reference point object using the given reference point creation
    function and point size.
    """
    create_ref_point()
    bpy.ops.transform.resize(value=(point_size, point_size, point_size))

    ref_point = bpy.context.object
    ref_point.name = ref_point_name

    return ref_point

def setup_dupliverts(plot_obj, ref_point):
    """
    Sets up dupliverts between the plot object and the reference point object,
    so that each of the verticies of the plot object have the shape of the
    reference point.
    """
    DUPLIVERTS = "VERTS"

    plot_obj.select = True
    ref_point.select = True

    bpy.context.scene.objects.active = plot_obj

    bpy.ops.object.parent_set()
    plot_obj.dupli_type = DUPLIVERTS

if __name__ == "__main__":
    main()
