"""Render the original embossed bee geometry with soft studio light.

Reproduce with Blender 3.3:
  blender --background --factory-startup --disable-autoexec --python render_bee_roller.py
The source is opened without saving, preserving the original file and geometry.
"""
from pathlib import Path
import bpy
from mathutils import Vector

SOURCE = Path(r'C:/Users/fredd/OneDrive/Desktop/3d roler files/more single fower/design 1/embossed bumblebee.blend')
OUTPUT = Path(__file__).resolve().parents[1] / 'dist/assets/blender-embossed-detail.png'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene = bpy.context.scene
roller = bpy.data.objects['Cylinder']
for obj in list(scene.objects):
    obj.hide_render = obj != roller

mat = bpy.data.materials.new('Soft blue gray ceramic')
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get('Principled BSDF')
bsdf.inputs['Base Color'].default_value = (0.32, 0.46, 0.51, 1)
bsdf.inputs['Roughness'].default_value = 0.64
bsdf.inputs['Specular'].default_value = 0.18
roller.data.materials.clear()
roller.data.materials.append(mat)
# No mesh, topology, modifier or relief changes.

def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

def area(name, location, energy, size, target, color=(1, 1, 1)):
    data = bpy.data.lights.new(name, 'AREA')
    data.energy = energy
    data.shape = 'DISK'
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    obj.location = location
    aim(obj, target)
    return obj

# Level view of the original upper diagonal bee, identified by UV (0.435, 0.800).
# Both wings remain visible; the roller's top edge is outside the frame.
target = (0, 0, 1.08)
camera_data = bpy.data.cameras.new('Bee detail camera')
camera = bpy.data.objects.new('Bee detail camera', camera_data)
scene.collection.objects.link(camera)
camera.location = (-7.942956, -18.355094, 1.08)
aim(camera, target)
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 7.6
camera.data.clip_end = 100
camera.data.dof.use_dof = False
scene.camera = camera
area('Broad soft key', (-5, -3, 7), 800, 4.8, target, (1.0, 0.97, 0.93))
area('Broad soft fill', (5, -5, 4), 270, 6.0, target, (0.92, 0.96, 1.0))
world = bpy.data.worlds.new('Soft pale studio')
world.use_nodes = True
world.node_tree.nodes.get('Background').inputs['Color'].default_value = (0.87, 0.91, 0.93, 1)
world.node_tree.nodes.get('Background').inputs['Strength'].default_value = 0.22
scene.world = world
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.025
scene.cycles.max_bounces = 4
scene.render.threads_mode = 'FIXED'
scene.render.threads = 12
scene.render.resolution_x = 640
scene.render.resolution_y = 1400
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = False
scene.render.filepath = str(OUTPUT)
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1
bpy.ops.render.render(write_still=True)
print(f'RENDERED {OUTPUT}; SOURCE {SOURCE}')




