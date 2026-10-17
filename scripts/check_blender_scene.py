#!/usr/bin/env python3
"""Executed inside Blender: check that a .blend contains working animated geometry."""
import bpy
from mathutils import Vector

scene=bpy.context.scene
assert scene.camera is not None,"Camera absent"
assert scene.frame_end>=12,"Too few frames"
assert scene.render.engine=="CYCLES","Headless render must use CPU Cycles"
assert len(bpy.data.materials)>=5,"Missing material palette"
hips=bpy.data.objects["Articulacao_right_hip"]
assert hips.animation_data and hips.animation_data.action,"No rig motion recorded"
scene.frame_set(1)
first=hips.location.copy()
scene.frame_set(4)
second=hips.location.copy()
assert (first-second).length>.12,"Rendered mannequin did not move"
for name in ("Tapete","Cabeca ilustrativa","Camera"):
    assert name in bpy.data.objects,"Missing scene object: "+name
for name in ("Articulacao_left_knee","Articulacao_right_knee"):
    assert name in bpy.data.objects
print("BLENDER_SCENE_PASS camera materials object tracks and dynamic 3D poses")
