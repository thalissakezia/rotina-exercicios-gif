#!/usr/bin/env python3
"""Local 3D interchange; never exports source tracks into a public directory."""
import argparse
import json
from pathlib import Path
from capture_utils import catalog_ids,load_capture
from world3d import make_blender_track

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=(ROOT/"work_private").resolve()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    out=args.out.resolve()
    if PRIVATE not in out.parents:
        parser.error("A saída com pontos de uma pessoa deve ficar em work_private/")
    data,_=load_capture(args.input,catalog_ids(ROOT))
    preview=make_blender_track(data)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(preview,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Pontos 3D transformados para visualização PRIVADA:",out)
    print("Revisão:",preview["review_status"],"• técnica certificada:",preview["technique_certified"])

if __name__=="__main__":main()
