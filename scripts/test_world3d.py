#!/usr/bin/env python3
"""Only synthetic 3D test points; NEVER a publishable movement example."""
import math
from copy import deepcopy
from capture_utils import CaptureError,validate_capture
from world3d import validate_world_track,make_blender_track

body={
 "shoulder":(.16,-.52,.02),"elbow":(.21,-.26,.02),
 "wrist":(.22,0,.02),"hip":(.13,0,0),
 "knee":(.13,.42,0),"ankle":(.13,.83,0)
}
frames=[]
for i in range(12):
    wave=.015*math.sin(i*math.pi/6)
    screen={}
    world={}
    for side in ("left","right"):
        sign=-1 if side=="left" else 1
        for name,(x,y,z) in body.items():
            key=side+"_"+name
            world[key]=[sign*x+wave,y,z,.98]
            screen[key]=[.5+sign*x*.4+wave,.45+y*.24,.98]
    frames.append({"time_ms":i*100,"landmarks":screen,"world_landmarks":world})
test={
 "schema_version":1,"exercise_id":"ponte",
 "source":{"kind":"video","label":"Test only","permission_confirmed":True,"sha256":"a"*64},
 "review":{"status":"pending"},"view":"lateral","sampling_fps":10,"frames":frames
}
assert validate_capture(test,{"ponte"})["technique_certified"] is False
assert validate_world_track(test)["raw_world_coordinates"]
result=make_blender_track(test)
assert result["format"]=="exercise-private-rig-preview-v1"
assert result["technique_certified"] is False and result["review_status"]=="pending"
assert len(result["frames"])==12
assert result["frames"][0]["joints"]["left_ankle"][2]>=0

def reject(fn):
    case=deepcopy(test)
    fn(case)
    try:validate_world_track(case)
    except CaptureError:return
    raise AssertionError("Invalid 3D landmarks accepted")
reject(lambda q:q["frames"][4].pop("world_landmarks"))
reject(lambda q:q["frames"][4]["world_landmarks"]["right_knee"].__setitem__(0,100.))
reject(lambda q:q["frames"][4]["world_landmarks"]["right_knee"].__setitem__(3,.1))
reject(lambda q:q["frames"][4]["world_landmarks"]["right_knee"].__setitem__(1,2.))
print("OK: synthetic 3D poses, preview transformations and error rejection.")
