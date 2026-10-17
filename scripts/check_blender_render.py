#!/usr/bin/env python3
"""Checks two actual Blender PNG renders from test-only landmarks."""
import sys
from pathlib import Path
from PIL import Image,ImageChops,ImageStat

a,b=map(Path,sys.argv[1:3])
assert a.is_file() and b.is_file(),"Missing rendered Blender PNG"
with Image.open(a) as f1,Image.open(b) as f2:
    im1=f1.convert("RGB")
    im2=f2.convert("RGB")
    assert im1.size==im2.size
    assert min(im1.size)>=200,"Render unexpectedly tiny"
    diff=ImageChops.difference(im1,im2)
    extrema=diff.getbbox()
    assert extrema is not None,"Two rendered frames are pixel-identical"
    rms=ImageStat.Stat(diff).rms
    score=sum(rms)/3
    assert score>.15,f"Blender output barely changes: RMS={score:.3f}"
    print(f"BLENDER_RENDER_PASS {im1.width}x{im1.height}; mean RMS difference={score:.3f}")
