import pandas as pd
import bpy

def main():
    data_file = "/home/chris/Datasets/hyg/hygdata_v3.csv"
    x_col = "x"
    y_col = "y"
    z_col = "z"
    scaling = 0.001     # Scaling factor for the range of data point positions
    point_size = 0.1    # Dimension size for a single point
    mesh_name = "Mesh"
    plot_name = "ScatterPlot"
    ref_point_name = "ReferencePoint"
    create_ref_point = bpy.ops.mesh.primitive_cube_add  # The function that creates a single reference point

    data = pd.read_csv(data_file)

    plot_dupliverts(data, x_col, y_col, z_col, scaling, point_size, mesh_name, plot_name, ref_point_name, create_ref_point)

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
        y = row[y_col] * scaling
        z = row[z_col] * scaling
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
