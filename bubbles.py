import bpy
from random import randint, uniform

# select and delete all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# set render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.shading_system = True

# set variables
frames = 40
frame_rate = 5
bubble_density = 10
bubble_rate = 4
lift_rate = 5

scene = bpy.context.scene
materials = bpy.data.materials

# reset frames
scene.frame_set(0)

# create camera
camera = bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-56, 53, 16), rotation=(1.84, 0.05, -1.59), scale=(1, 1, 1))

# create plane
bpy.ops.mesh.primitive_plane_add(size=100, enter_editmode=False, align='WORLD', location=(60, 50, 50), rotation=(0, 1.5, 0), scale=(1, 1, 1))


def clear_material(material):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()
        
def instanciate_group( nodes, group_name ):
    group = nodes.new( type = 'ShaderNodeGroup' )
    group.node_tree = bpy.data.node_groups[group_name]
    


def bubble_birth():
    x = randint(0, 50)
    y = randint(0, 100)
    z = randint(0, 10)
    
    r = uniform(0.6, 0.9)
    g = uniform(0.6, 0.9)
    b = uniform(0.6, 0.9)
#    
#   create sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=100, ring_count=50,enter_editmode=False, align='WORLD', location=(x, y, z), scale=(1, 1, 1))
    
#   turn off motion blur
    bpy.context.object.cycles.use_motion_blur = False
    
#   create material
    mat = bpy.data.materials.new(name="Mats")
    mat.use_nodes = True
    bpy.context.object.active_material = mat
    
#   remove principled node
    clear_material(mat)
    
#   create glass node
    glass_node = mat.node_tree.nodes.new('ShaderNodeBsdfGlass')
    glass_node.inputs[0].default_value = (r, g, b, 1)
    
#   link to outputs
    nodes = mat.node_tree.nodes
    material_output = nodes.get("Material Output")
    if material_output is None:
        material_output = nodes.new("ShaderNodeOutputMaterial")
    links = mat.node_tree.links
    links.new(material_output.inputs["Surface"], glass_node.outputs["BSDF"])
    
def lift_bubbles():
    for collection in bpy.data.collections:
       for obj in collection.all_objects:
           if 'Sphere' in obj.name:
               bpy.data.objects[obj.name].select_set(True)
               obj.location[2] += lift_rate
               
               
for frame in range(frames):
    
    f = frame * frame_rate    
    
    for bubble in range(bubble_density):
        bubble_birth()
        
    bpy.ops.object.select_all(action='SELECT')
    all = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    
    for obj in all:
        obj.keyframe_insert(data_path="location", frame=f)
    
    lift_bubbles()