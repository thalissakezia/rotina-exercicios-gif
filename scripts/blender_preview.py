#!/usr/bin/env python3
"""Private Blender mannequin preview from world landmarks, NOT an instructional GIF.
Run: blender -b --python scripts/blender_preview.py -- --input PATH --out PATH
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import bpy
    from mathutils import Vector
except ImportError:
    raise SystemExit("Run with Blender, not standard Python.")

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=(ROOT/"work_private").resolve()
PAIRS=[
    ("left_shoulder","left_elbow"),("left_elbow","left_wrist"),
    ("right_shoulder","right_elbow"),("right_elbow","right_wrist"),
    ("left_hip","left_knee"),("left_knee","left_ankle"),
    ("right_hip","right_knee"),("right_knee","right_ankle"),
    ("left_shoulder","right_shoulder"),("left_hip","right_hip"),
    ("left_shoulder","left_hip"),("right_shoulder","right_hip")
]
JOINTS={name for pair in PAIRS for name in pair}

def private_path(path):
    p=Path(path).resolve()
    if PRIVATE not in p.parents:
        raise ValueError("Only paths under work_private/ are permitted")
    return p

def material(name,color):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1.)
    m.use_nodes=True
    shader=m.node_tree.nodes.get("Principled BSDF")
    if shader:shader.inputs["Base Color"].default_value=(*color,1.)
    return m

def sphere(name,rad,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=10,radius=rad)
    o=bpy.context.object
    o.name=name
    o.data.materials.append(mat)
    return o

def rod(name,rad,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=rad,depth=1.)
    o=bpy.context.object
    o.name=name
    o.rotation_mode="QUATERNION"
    o.data.materials.append(mat)
    return o

def make_scene(data):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    frames=data["frames"]
    scene.render.resolution_x=900
    scene.render.resolution_y=900
    scene.render.resolution_percentage=70
    scene.render.image_settings.file_format="PNG"
    scene.render.engine="CYCLES"
    scene.cycles.device="CPU"
    scene.cycles.samples=8
    scene.render.film_transparent=False
    scene.render.fps=max(2,round(data["fps"]))
    scene.frame_start=1
    scene.frame_end=len(frames)
    scene.world.color=(.94,.94,.97)
    pink=material("Top rosa",(.92,.29,.54))
    navy=material("Legging azul marinho",(.08,.14,.30))
    skin=material("Pele ilustrativa",(.8,.57,.43))
    shoes=material("Tenis rosa",(.95,.55,.68))
    purple=material("Tapete lilas",(.56,.43,.85))
    hair=material("Cabelo escuro",(.21,.17,.2))
    joint_objects={}
    for name in sorted(JOINTS):
        color=(shoes if name.endswith("ankle")
               else navy if name.endswith(("knee","hip"))
               else pink if name.endswith("shoulder") else skin)
        joint_objects[name]=sphere("Articulacao_"+name,.058,color)
    segments={}
    for a,b in PAIRS:
        color=(navy if a.endswith(("hip","knee")) or b.endswith(("knee","ankle"))
               else pink if a.endswith("shoulder") and b.endswith("hip")
               else skin)
        segments[(a,b)]=rod("Segmento_"+a+"_"+b,.054,color)
    head=sphere("Cabeca ilustrativa",.13,skin)
    pony=sphere("Coque estilizado",.075,hair)
    bpy.ops.mesh.primitive_cube_add(size=1)
    ground=bpy.context.object
    ground.name="Tapete"
    ground.scale=(2.8,1.65,.035)
    ground.location=(0,0,-.04)
    ground.data.materials.append(purple)
    for i,frame in enumerate(frames,1):
        scene.frame_set(i)
        joints={k:Vector(v) for k,v in frame["joints"].items()}
        for name,obj in joint_objects.items():
            obj.location=joints[name]
            obj.keyframe_insert(data_path="location",frame=i)
        for (a,b),obj in segments.items():
            start,end=joints[a],joints[b]
            delta=end-start
            if delta.length<.001:
                raise ValueError("A segment has zero length")
            obj.location=(start+end)/2
            obj.rotation_quaternion=delta.to_track_quat("Z","Y")
            obj.scale=(1.,1.,delta.length)
            obj.keyframe_insert(data_path="location",frame=i)
            obj.keyframe_insert(data_path="rotation_quaternion",frame=i)
            obj.keyframe_insert(data_path="scale",frame=i)
        shoulders=(joints["left_shoulder"]+joints["right_shoulder"])/2
        head.location=shoulders+Vector((0,0,.22))
        pony.location=head.location+Vector((0,.11,.085))
        head.keyframe_insert(data_path="location",frame=i)
        pony.keyframe_insert(data_path="location",frame=i)
    bpy.ops.object.camera_add(location=(2.6,-4.6,2.5))
    cam=bpy.context.object
    target=Vector((0,0,.8))
    cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.type="ORTHO"
    cam.data.ortho_scale=3.4
    scene.camera=cam
    bpy.ops.object.light_add(type="AREA",location=(1,-3,4))
    lamp=bpy.context.object
    lamp.data.energy=600
    lamp.data.shape="DISK"
    lamp.data.size=5
    scene.frame_set(1)
    return scene

def main():
    cli=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--render-still",action="store_true")
    args=p.parse_args(cli)
    source=private_path(args.input)
    out=private_path(args.out)
    if out.suffix.lower()!=".blend":p.error("Output must have .blend extension")
    data=json.loads(source.read_text(encoding="utf-8"))
    if data.get("format")!="exercise-private-rig-preview-v1":
        p.error("Invalid input format")
    if data.get("review_status")!="pending" or data.get("technique_certified") is not False:
        p.error("Preview must remain pending, not approved")
    frames=data.get("frames")
    if not isinstance(frames,list) or not 8<=len(frames)<=180:
        p.error("Invalid number of frames")
    if any(not isinstance(f.get("joints"),dict) or set(f["joints"])!=JOINTS for f in frames):
        p.error("Missing required joints")
    out.parent.mkdir(parents=True,exist_ok=True)
    scene=make_scene(data)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    if args.render_still:
        scene.render.filepath=str(out.with_name(out.stem+"_PREVIEW_NOT_VALIDATED.png"))
        bpy.ops.render.render(write_still=True)
    print("Saved PRIVATE 3D mannequin preview; technique NOT validated:",out)

if __name__=="__main__":
    main()
