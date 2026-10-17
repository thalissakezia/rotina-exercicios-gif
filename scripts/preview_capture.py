#!/usr/bin/env python3
"""Watermarked local stick-figure preview. NOT a certified exercise GIF."""
import argparse
import json
from pathlib import Path
from PIL import Image,ImageDraw
from capture_utils import catalog_ids,load_capture

ROOT=Path(__file__).resolve().parents[1]
BONES=(("shoulder","elbow"),("elbow","wrist"),("shoulder","hip"),("hip","knee"),("knee","ankle"))

def render(data,side,out):
    result=[]
    for i,frame in enumerate(data["frames"]):
        im=Image.new("RGB",(480,520),"#fff8fc")
        d=ImageDraw.Draw(im)
        d.text((18,15),"PRÉVIA • NÃO VALIDADA",fill="#c0226a")
        d.text((18,42),"Captura de: "+data["exercise_id"][:31],fill="#132653")
        d.rounded_rectangle((15,80,465,445),radius=20,fill="#eaf2fb")
        coords=frame["landmarks"]
        def xy(j):
            x,y,_=coords[side+"_"+j]
            return int(25+x*430),int(84+y*344)
        for a,b in BONES:
            d.line((*xy(a),*xy(b)),fill="#274c8a",width=12)
        for joint in ("shoulder","elbow","wrist","hip","knee","ankle"):
            x,y=xy(joint)
            d.ellipse((x-8,y-8,x+8,y+8),fill="#e73679",outline="#152b55",width=2)
        d.text((18,469),f"Quadro {i+1}/{len(data['frames'])} · Pontos extraídos de vídeo",fill="#132653")
        d.text((18,494),"Esqueleto 2D, sem revisão biomecânica",fill="#a3236b")
        result.append(im)
    out.parent.mkdir(parents=True,exist_ok=True)
    result[0].save(out,save_all=True,append_images=result[1:],
                   loop=0,duration=100,disposal=2,optimize=False)
    return len(result)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    out=args.out.resolve()
    if ROOT.resolve() in out.parents and (ROOT/"work_private").resolve() not in out.parents:
        p.error("Saída local dentro do projeto somente em work_private/")
    data,quality=load_capture(args.input,catalog_ids(ROOT))
    n=render(data,quality["side"],out)
    print(json.dumps({"preview":str(out),"frames":n,"review":"pending","approved":False},ensure_ascii=False))

if __name__=="__main__":main()
