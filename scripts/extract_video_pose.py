#!/usr/bin/env python3
"""Extract local video landmarks using optional MediaPipe Tasks, no uploads."""
import argparse
import hashlib
import json
from pathlib import Path
from capture_utils import catalog_ids,validate_capture

ROOT=Path(__file__).resolve().parents[1]
INDICES=(11,12,13,14,15,16,23,24,25,26,27,28)
NAMES=("left_shoulder","right_shoulder","left_elbow","right_elbow",
       "left_wrist","right_wrist","left_hip","right_hip",
       "left_knee","right_knee","left_ankle","right_ankle")

def main():
    p=argparse.ArgumentParser(description="Vídeo autorizado -> dados de pose privados")
    p.add_argument("--video",required=True,type=Path)
    p.add_argument("--model",required=True,type=Path,help="Modelo .task local, sem download automático")
    p.add_argument("--exercise-id",required=True)
    p.add_argument("--source-label",required=True)
    p.add_argument("--rights-confirmed",action="store_true")
    p.add_argument("--view",required=True,choices=("lateral","frontal","obliqua"))
    p.add_argument("--fps",type=float,default=10.)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    if not args.rights_confirmed:p.error("Falta --rights-confirmed")
    if args.exercise_id not in catalog_ids(ROOT):p.error("Exercício não cadastrado")
    if not args.video.is_file() or not args.model.is_file():p.error("Vídeo/modelo ausente")
    if not 2<=args.fps<=30:p.error("FPS permitido: 2 a 30")
    out=args.out.resolve()
    if ROOT.resolve() in out.parents and (ROOT/"work_private").resolve() not in out.parents:
        p.error("Dentro do projeto, saída permitida apenas em work_private/")
    try:
        import cv2
        import mediapipe as mp
    except ImportError as exc:
        p.error("Instale pip install -r requirements-capture.txt: "+str(exc))
    digest=hashlib.sha256()
    with args.video.open("rb") as f:
        for part in iter(lambda:f.read(1024*1024),b""):digest.update(part)
    cap=cv2.VideoCapture(str(args.video))
    if not cap.isOpened():p.error("Falha ao abrir vídeo")
    source_fps=cap.get(cv2.CAP_PROP_FPS)
    if not source_fps or source_fps<args.fps:
        cap.release();p.error("FPS original insuficiente")
    options=mp.tasks.vision.PoseLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(args.model)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,num_poses=1)
    frames=[];next_t=0.;index=0
    try:
        with mp.tasks.vision.PoseLandmarker.create_from_options(options) as detector:
            while len(frames)<180:
                ok,bgr=cap.read()
                if not ok:break
                timestamp=index*1000/source_fps
                index+=1
                if timestamp+1e-6<next_t:continue
                next_t+=1000/args.fps
                t=round(timestamp)
                if frames and t<=frames[-1]["time_ms"]:continue
                rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
                img=mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb)
                result=detector.detect_for_video(img,t)
                if not result.pose_landmarks:
                    p.error("Corpo não detectado; enquadre o corpo inteiro sem cortes")
                landmarks=result.pose_landmarks[0]
                joint_data={name:[float(landmarks[j].x),float(landmarks[j].y),
                                  float(landmarks[j].visibility or 0)] for name,j in zip(NAMES,INDICES)}
                frames.append({"time_ms":t,"landmarks":joint_data})
    finally:
        cap.release()
    record={
        "schema_version":1,"exercise_id":args.exercise_id,
        "source":{"kind":"video","label":args.source_label,
                  "permission_confirmed":True,"sha256":digest.hexdigest()},
        "view":args.view,"sampling_fps":args.fps,
        "review":{"status":"pending"},"frames":frames
    }
    report=validate_capture(record,catalog_ids(ROOT))
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"arquivo_privado":str(out),"resultado":report},ensure_ascii=False))
    print("NÃO APROVADO: a execução exige revisão humana antes de virar material de treino.")

if __name__=="__main__":main()
