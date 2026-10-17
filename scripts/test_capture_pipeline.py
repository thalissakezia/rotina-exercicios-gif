#!/usr/bin/env python3
"""Software-only fixtures; do not publish them as exercise motion references."""
import math
import tempfile
from copy import deepcopy
from pathlib import Path
from PIL import Image
from capture_utils import catalog_ids,validate_capture,CaptureError
from preview_capture import render

ROOT=Path(__file__).resolve().parents[1]
ids=catalog_ids(ROOT)
assert "ponte" in ids
base={"shoulder":(.28,.54),"elbow":(.26,.68),"wrist":(.23,.83),
      "hip":(.53,.56),"knee":(.70,.70),"ankle":(.79,.85)}
frames=[]
for i in range(12):
    t=(1-math.cos(math.pi*2*i/12))/2
    landmarks={}
    for side in ("left","right"):
        for joint,(x,y) in base.items():
            delta=-.03*t if joint in ("hip","knee") else 0
            landmarks[side+"_"+joint]=[x+(.01 if side=="right" else 0),y+delta,.96]
    frames.append({"time_ms":100*i,"landmarks":landmarks})
sample={"schema_version":1,"exercise_id":"ponte",
        "source":{"kind":"video","label":"teste sintético não publicável",
                  "permission_confirmed":True,"sha256":"a"*64},
        "review":{"status":"pending"},"view":"lateral",
        "sampling_fps":10,"frames":frames}
info=validate_capture(sample,ids)
assert info["frames"]==12 and info["technique_certified"] is False
with tempfile.TemporaryDirectory() as d:
    dest=Path(d)/"preview.gif"
    assert render(sample,info["side"],dest)==12
    with Image.open(dest) as gif:
        assert gif.n_frames==12 and gif.size==(480,520)

def reject(fn):
    data=deepcopy(sample)
    fn(data)
    try:
        validate_capture(data,ids)
    except CaptureError:
        return
    raise AssertionError("Dados inválidos aceitos indevidamente")

reject(lambda x:x.update(exercise_id="nao-existe"))
reject(lambda x:x["source"].update(permission_confirmed=False))
reject(lambda x:x["review"].update(status="approved"))
reject(lambda x:x["frames"][4].update(time_ms=0))
reject(lambda x:x["frames"][6]["landmarks"]["right_knee"].__setitem__(0,2))
reject(lambda x:[x["frames"][6]["landmarks"][s+"_hip"].__setitem__(0,.9)
                 for s in ("left","right")])
print("OK: prévia sintética com 12 quadros; direitos, IDs, tempos, saltos e falsa aprovação bloqueados.")
