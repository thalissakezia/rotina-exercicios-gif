#!/usr/bin/env python3
"""Convert Blender PNGs to PRIVATE animated GIF + review contact sheet.

The visible watermark cannot be disabled via CLI, and results are NEVER
silently copied into output/gifs. Not a biomechanical certification.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=(ROOT/"work_private").resolve()
WARN="PREVIA 3D - NAO VALIDADA"
SYNTH="TESTE SINTETICO - NAO E EXERCICIO"

def is_private(path):
    q=Path(path).resolve()
    if PRIVATE not in q.parents:
        raise ValueError("Dados/previas do Blender devem ficar em work_private/")
    return q

def font(size):
    try:return ImageFont.truetype("DejaVuSans-Bold.ttf",size)
    except OSError:return ImageFont.load_default()

def draw_warning(im,test_only):
    im=im.convert("RGB")
    d=ImageDraw.Draw(im)
    w,h=im.size
    band=max(45,int(h*.10))
    d.rectangle((0,0,w,band),fill="#142456")
    d.text((12,10),SYNTH if test_only else WARN,font=font(max(13,w//33)),fill="white")
    d.rectangle((0,h-29,w,h),fill="#fff1f6")
    d.text((12,h-25),"Revisao de movimento pendente",font=font(max(12,w//50)),fill="#a72161")
    return im

def render(frames,out_gif,out_sheet,test_only=False):
    frames=[Path(p) for p in frames]
    if not 8<=len(frames)<=180:raise ValueError("Exigidos de 8 a 180 frames")
    images=[]
    w=h=None
    for p in frames:
        with Image.open(p) as loaded:
            loaded.load()
            im=loaded.convert("RGB")
        if w is None:w,h=im.size
        if im.size!=(w,h):raise ValueError("Quadros com dimensoes distintas")
        if min(im.size)<200:raise ValueError("Quadro pequeno demais")
        images.append(draw_warning(im,test_only))
    if not any(ImageChops.difference(im,images[0]).getbbox() for im in images[1:]):
        raise ValueError("Todos os quadros da animacao sao identicos")
    out_gif=Path(out_gif);out_sheet=Path(out_sheet)
    for p in (out_gif,out_sheet):p.parent.mkdir(parents=True,exist_ok=True)
    pal=[im.quantize(colors=112,method=Image.Quantize.FASTOCTREE) for im in images]
    pal[0].save(out_gif,save_all=True,append_images=pal[1:],
                duration=100,loop=0,optimize=False,disposal=2)
    idx=sorted({round((len(images)-1)*i/5) for i in range(6)})
    tw,th=round(w*.35),round(h*.35)
    sheet=Image.new("RGB",(tw*3,th*2+52),"#fffafb")
    for i,n in enumerate(idx):
        pic=images[n].resize((tw,th),Image.Resampling.LANCZOS)
        sheet.paste(pic,((i%3)*tw,(i//3)*th+52))
    ImageDraw.Draw(sheet).text((15,12),SYNTH if test_only else WARN,
                               font=font(18),fill="#b3266a")
    sheet.save(out_sheet)
    return {"frames":len(images),"size":[w,h],"gif_bytes":out_gif.stat().st_size,
            "contact_sheet":str(out_sheet),"review_status":"pending",
            "approved_for_training":False,"synthetic_test_only":bool(test_only)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--frames-dir",required=True,type=Path)
    p.add_argument("--prefix",default="review_")
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--contact-sheet",required=True,type=Path)
    p.add_argument("--test-only",action="store_true")
    a=p.parse_args()
    try:
        src=is_private(a.frames_dir);dest=is_private(a.out)
        sheet=is_private(a.contact_sheet)
    except ValueError as err:p.error(str(err))
    files=sorted(src.glob(a.prefix+"*.png"))
    result=render(files,dest,sheet,a.test_only)
    print(json.dumps(result,ensure_ascii=False))
    print("Arquivos de revisao continuam privados. Publicacao automatica: NAO.")

if __name__=="__main__":main()
