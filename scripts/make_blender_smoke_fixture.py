#!/usr/bin/env python3
"""Temporary TEST-ONLY landmarks. Not a true exercise or approved reference."""
import json
import math
from copy import deepcopy
from pathlib import Path
from test_world3d import test
from world3d import make_blender_track

ROOT=Path(__file__).resolve().parents[1]
case=deepcopy(test)
for i,frame in enumerate(case["frames"]):
    offset=.18*math.sin(2*math.pi*i/12)
    for point in frame["world_landmarks"].values():
        point[0]+=offset
track=make_blender_track(case)
track["synthetic_test_only"]=True
track["source_label"]="SYNTHETIC SOFTWARE TEST -- NO EXERCISE DEMONSTRATION"
out=ROOT/"work_private"/"rig"/"smoke-test.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(track,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("Synthetic 3D fixture:",out,"frames:",len(track["frames"]))
