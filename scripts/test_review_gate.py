#!/usr/bin/env python3
"""Synthetic unit tests only; no medical/sports expertise is claimed."""
from pathlib import Path
import tempfile
import math
import json
from copy import deepcopy
from datetime import datetime, timezone
from PIL import Image,ImageDraw
from capture_utils import CaptureError
from approval_gate import CHECKS, gate, digest
from render_review_gif import render

with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    frames=[]
    for i in range(12):
        p=root/f"frame_{i:04d}.png"
        im=Image.new("RGB",(280,280),"#fff8ef")
        draw=ImageDraw.Draw(im)
        draw.ellipse((20+5*i,90,90+5*i,160),fill="#cd4488")
        im.save(p)
        frames.append(p)
    gif=root/"preview.gif"
    sheet=root/"sheet.png"
    result=render(frames,gif,sheet,test_only=True)
    assert result["frames"]==12 and not result["approved_for_training"]
    with Image.open(gif) as g:
        assert g.n_frames>=10
    with Image.open(sheet) as im:assert im.size[0]>200
    try:render([frames[0]]*12,root/"bad.gif",root/"bad.png",False)
    except ValueError:pass
    else:raise AssertionError("Accepted identical frames")
    rights={"schema_version":1,"exercises":{"ponte":{
        "permission_confirmed":True,"person_consented":True,
        "basis":"own_recording","source_label":"SYNTHETIC TEST","view":"lateral"}}}
    pose={"shoulder":(.25,.40),"elbow":(.25,.55),"wrist":(.25,.70),
          "hip":(.50,.45),"knee":(.65,.60),"ankle":(.78,.72)}
    seq=[]
    for i in range(12):
        pts={}
        for side in ("left","right"):
            for joint,(x,y) in pose.items():
                pts[side+"_"+joint]=[x+(.001*i),y,.99]
        seq.append({"time_ms":i*100,"landmarks":pts})
    cap={"schema_version":1,"exercise_id":"ponte",
         "source":{"kind":"video","label":"SYNTHETIC TEST","permission_confirmed":True,
                   "sha256":"a"*64},"view":"lateral","sampling_fps":10,
         "review":{"status":"pending"},"frames":seq}
    signed={"schema_version":1,"exercise_id":"ponte","source_sha256":"a"*64,
            "preview_sha256":digest(gif),"decision":"approve_for_private_staging",
            "reviewed_at":datetime.now(timezone.utc).isoformat(),
            "reviewer":{"name":"Example Reviewer","qualification":"Example qualification",
                        "notes":"SYNTHETIC DATA ONLY. Software schema test."},
            "checklist":{name:True for name in CHECKS}}
    eligible=gate(signed,cap,rights,{"ponte"},digest(gif))
    assert eligible["status"]=="eligible_for_manual_private_staging"
    assert eligible["automatic_publication"] is False
    def should_block(modify):
        c=deepcopy(signed);r=deepcopy(rights);pose=deepcopy(cap)
        modify(c,r,pose)
        try:gate(c,pose,r,{"ponte"},digest(gif))
        except (CaptureError,ValueError):return
        raise AssertionError("Invalid review accepted")
    should_block(lambda s,r,c:s.update(preview_sha256="b"*64))
    should_block(lambda s,r,c:s.update(exercise_id="coice"))
    should_block(lambda s,r,c:s["checklist"].update(pelvis_spine_checked=False))
    should_block(lambda s,r,c:s.update(decision="pending"))
    should_block(lambda s,r,c:r["exercises"]["ponte"].update(person_consented=False))
    should_block(lambda s,r,c:s.update(synthetic_test_only=True))
    should_block(lambda s,r,c:c.update(synthetic_test_only=True))
    should_block(lambda s,r,c:s.update(reviewer={}))
    should_block(lambda s,r,c:s.update(reviewed_at="yesterday"))
print("OK: full review GIF + contact sheet, hash gate, rights and explicit checklist; no auto-publication.")
