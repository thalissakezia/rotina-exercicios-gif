#!/usr/bin/env python3
"""Batch-authorized LOCAL capture. Never uploads/auto-publishes private media."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from capture_utils import catalog_ids

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=(ROOT/"work_private").resolve()
EXTENSIONS={".mp4",".mov",".avi",".m4v"}
BASIS={"own_recording","written_license","cc_license"}

def inside_private(path):
    p=Path(path).resolve()
    if PRIVATE not in p.parents:
        raise ValueError("Use apenas caminhos dentro de work_private/")
    return p

def candidates(video_dir,rights,valid_ids):
    """Return candidates with an explicit authorization gate for EVERY video."""
    video_dir=Path(video_dir)
    result=[]
    for path in sorted(video_dir.glob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        eid=path.stem
        note=rights.get(eid,{})
        reason=None
        if eid not in valid_ids:reason="exercício não cadastrado"
        elif note.get("permission_confirmed") is not True:
            reason="autorização de uso não confirmada"
        elif note.get("person_consented") is not True:
            reason="consentimento da pessoa filmada não confirmado"
        elif note.get("basis") not in BASIS:
            reason="base da autorização desconhecida"
        elif not isinstance(note.get("source_label"),str) or not note["source_label"].strip():
            reason="origem não documentada"
        elif note.get("view") not in ("frontal","lateral","obliqua"):
            reason="ângulo da câmera não documentado"
        elif note.get("basis")=="cc_license" and not str(note.get("license_url","")).startswith("https://"):
            reason="licença aberta sem endereço verificável"
        result.append({"exercise_id":eid,"video":path,"rights":note,
                       "ready_for_local_preview":reason is None,"blocked_reason":reason})
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--video-dir",type=Path,default=PRIVATE/"videos")
    p.add_argument("--permissions",type=Path,default=PRIVATE/"video_permissions.json")
    p.add_argument("--model",type=Path,default=PRIVATE/"pose_landmarker.task")
    p.add_argument("--run",action="store_true",help="Executar capturas; sem --run apenas lista")
    args=p.parse_args()
    try:
        video_dir=inside_private(args.video_dir)
        manifest=inside_private(args.permissions)
        model=inside_private(args.model)
    except ValueError as exc:p.error(str(exc))
    if not manifest.is_file():p.error("Crie work_private/video_permissions.json conforme docs/LOTE-DE-VIDEOS.md")
    try:
        data=json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("schema_version")!=1 or not isinstance(data.get("exercises"),dict):
            p.error("Manifesto de direitos inválido")
    except json.JSONDecodeError as exc:p.error("Manifesto não é JSON: "+str(exc))
    found=candidates(video_dir,data["exercises"],catalog_ids(ROOT))
    if not found:
        print("Nenhum vídeo local encontrado. Fila técnica permanece pendente.")
        return
    approved=0; blocked=0
    for item in found:
        eid=item["exercise_id"]
        if not item["ready_for_local_preview"]:
            blocked+=1
            print("BLOQUEADO:",eid,":",item["blocked_reason"])
            continue
        print("APTO À PRÉVIA PRIVADA (NÃO VALIDADA):",eid)
        if not args.run:continue
        if not model.is_file():p.error("Modelo MediaPipe .task ausente")
        note=item["rights"]
        capture=PRIVATE/"captures"/f"{eid}.json"
        scene=PRIVATE/"rig"/f"{eid}.json"
        extract=[
          sys.executable,str(ROOT/"scripts/extract_video_pose.py"),
          "--video",str(item["video"]),"--model",str(model),
          "--exercise-id",eid,"--source-label",note["source_label"],
          "--rights-confirmed","--view",note["view"],"--out",str(capture)
        ]
        subprocess.run(extract,check=True,cwd=ROOT)
        subprocess.run([
          sys.executable,str(ROOT/"scripts/prepare_blender_motion.py"),
          "--input",str(capture),"--out",str(scene)
        ],check=True,cwd=ROOT)
        approved+=1
    print(json.dumps({"candidates":len(found),"blocked":blocked,
                      "generated_private_previews":approved,
                      "automatic_publication":False},ensure_ascii=False))

if __name__=="__main__":main()
