"""Private capture schema; detects file errors, not clinical technique."""
from __future__ import annotations
import json
import math
import re
from pathlib import Path

JOINTS=tuple(f"{s}_{j}" for s in ("left","right") for j in
             ("shoulder","elbow","wrist","hip","knee","ankle"))
SIDE_JOINTS=("shoulder","elbow","wrist","hip","knee","ankle")
LIMBS=(("shoulder","elbow"),("elbow","wrist"),("hip","knee"),("knee","ankle"))

class CaptureError(ValueError): pass

def _finite(v):
    return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)

def catalog_ids(root:Path):
    content=json.loads((root/"data/exercicios.json").read_text(encoding="utf-8"))
    return {x["id"] for x in content["exercicios"]}

def validate_capture(data:dict,valid_ids:set[str]):
    """Rejects untrusted tracks. NEVER certifies a movement biomechanically."""
    if not isinstance(data,dict) or data.get("schema_version")!=1:
        raise CaptureError("Versão de esquema inválida")
    exid=data.get("exercise_id")
    if exid not in valid_ids:
        raise CaptureError("Exercício não cadastrado; associação negada")
    src=data.get("source")
    if not isinstance(src,dict) or src.get("kind")!="video" or src.get("permission_confirmed") is not True:
        raise CaptureError("Origem do vídeo e autorização explícita são obrigatórias")
    if not isinstance(src.get("label"),str) or not src["label"].strip():
        raise CaptureError("Descreva a origem")
    if not isinstance(src.get("sha256"),str) or not re.fullmatch("[a-f0-9]{64}",src["sha256"]):
        raise CaptureError("SHA256 obrigatório")
    if data.get("review",{}).get("status")!="pending":
        raise CaptureError("A captura não pode ser aprovada automaticamente")
    if data.get("view") not in ("lateral","frontal","obliqua"):
        raise CaptureError("Ângulo inválido")
    fps=data.get("sampling_fps")
    if not _finite(fps) or not 2<=fps<=30:
        raise CaptureError("FPS inválido")
    frames=data.get("frames")
    if not isinstance(frames,list) or not 8<=len(frames)<=180:
        raise CaptureError("É obrigatório ter 8 a 180 quadros")
    last=-1; available=[]
    for i,fr in enumerate(frames):
        t=fr.get("time_ms") if isinstance(fr,dict) else None
        if not isinstance(t,int) or t<=last or (last>=0 and t-last>700):
            raise CaptureError(f"Tempos inválidos no quadro {i}")
        last=t
        landmarks=fr.get("landmarks")
        if not isinstance(landmarks,dict) or not landmarks:
            raise CaptureError("Pontos corporais ausentes")
        for name,point in landmarks.items():
            if name not in JOINTS or not isinstance(point,list) or len(point)!=3:
                raise CaptureError(f"Ponto não permitido: {name}")
            if any(not _finite(v) for v in point) or any(v<0 or v>1 for v in point):
                raise CaptureError(f"Ponto fora do enquadramento: {name}")
        valid_sides={side for side in ("left","right") if all(
            side+"_"+j in landmarks and landmarks[side+"_"+j][2]>=.55 for j in SIDE_JOINTS)}
        if not valid_sides:
            raise CaptureError(f"Nenhum lado confiável no quadro {i}")
        available.append(valid_sides)
    common=set.intersection(*available)
    if not common:
        raise CaptureError("Nenhum lado corporal estável no vídeo inteiro")
    side="right" if "right" in common else "left"
    max_jump=0.
    for j in SIDE_JOINTS:
        points=[f["landmarks"][side+"_"+j] for f in frames]
        for a,b in zip(points,points[1:]):
            jump=math.hypot(a[0]-b[0],a[1]-b[1])
            if jump>.20:
                raise CaptureError(f"Salto excessivo no ponto {side}_{j}")
            max_jump=max(max_jump,jump)
    for a,b in LIMBS:
        lengths=[math.hypot(f["landmarks"][side+"_"+a][0]-f["landmarks"][side+"_"+b][0],
                            f["landmarks"][side+"_"+a][1]-f["landmarks"][side+"_"+b][1]) for f in frames]
        median=sorted(lengths)[len(lengths)//2]
        if median<.012 or any(v<.45*median or v>1.9*median for v in lengths):
            raise CaptureError(f"Segmento corporal inconsistente: {a}-{b}")
    return {"exercise_id":exid,"frames":len(frames),"side":side,
            "duration_s":round((frames[-1]["time_ms"]-frames[0]["time_ms"])/1000,2),
            "max_jump":round(max_jump,4),"review":"pending","technique_certified":False}

def load_capture(path:Path,valid_ids:set[str]):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    return data,validate_capture(data,valid_ids)
