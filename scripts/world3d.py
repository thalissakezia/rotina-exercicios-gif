"""Validate optional 3D landmarks; quality checks do not certify biomechanics."""
from math import hypot, isfinite
from capture_utils import CaptureError, JOINTS, LIMBS

REQUIRED=tuple(JOINTS)
JOINT_IDS=("shoulder","elbow","wrist","hip","knee","ankle")

def validate_world_track(record):
    frames=record.get("frames") or []
    if len(frames)<8:
        raise CaptureError("Vídeo curto demais para visualização 3D")
    max_jump=0.
    for ix,fr in enumerate(frames):
        points=fr.get("world_landmarks")
        if not isinstance(points,dict) or set(points)!=set(REQUIRED):
            raise CaptureError("Não há pontos 3D completos e sincronizados no quadro "+str(ix))
        for name,p in points.items():
            if not isinstance(p,list) or len(p)!=4 or not all(
                isinstance(v,(int,float)) and not isinstance(v,bool) and isfinite(v) for v in p
            ):
                raise CaptureError("Ponto 3D malformado: "+name)
            if any(abs(v)>4 for v in p[:3]) or not 0<=p[3]<=1:
                raise CaptureError("Coordenadas 3D fora dos limites: "+name)
            if p[3]<.55:
                raise CaptureError("Confiança 3D insuficiente: "+name)
        if ix:
            prev=frames[ix-1]["world_landmarks"]
            for name,p in points.items():
                a=prev[name]
                jump=sum((p[j]-a[j])**2 for j in range(3))**.5
                if jump>.45:
                    raise CaptureError("Salto 3D não plausível: "+name)
                max_jump=max(jump,max_jump)
    for side in ("left","right"):
        for aa,bb in LIMBS:
            a,b=side+"_"+aa,side+"_"+bb
            lengths=[]
            for fr in frames:
                pa,pb=fr["world_landmarks"][a],fr["world_landmarks"][b]
                lengths.append(sum((pa[j]-pb[j])**2 for j in range(3))**.5)
            median=sorted(lengths)[len(lengths)//2]
            if median<.04 or any(v<.60*median or v>1.6*median for v in lengths):
                raise CaptureError("Segmento instável: "+a+"—"+b)
    return {"num_frames":len(frames),"max_jump_m":round(max_jump,3),
            "raw_world_coordinates":True,"technique_certified":False}

def to_blender_space(point):
    # MediaPipe: x right, y down, z depth. Blender: z up.
    return [round(point[0],6),round(-point[2],6),round(-point[1],6)]

def make_blender_track(record):
    """Produces UNAPPROVED rig-input, with explicit privacy and review gates."""
    checks=validate_world_track(record)
    src=record["source"]
    fps=record["sampling_fps"]
    frames=[]
    for fr in record["frames"]:
        pts={j:to_blender_space(p) for j,p in fr["world_landmarks"].items()}
        frames.append({"time_ms":fr["time_ms"],"joints":pts})
    minimum=min(
        pt[2] for fr in frames for name,pt in fr["joints"].items()
        if name.endswith(("ankle","knee","wrist"))
    )
    # Align lowest observed extremity to a floor in the preview;
    # this is NOT a claim of measured physical foot-to-floor contact.
    for fr in frames:
        fr["joints"]={name:[p[0],p[1],round(p[2]-minimum,6)]
                      for name,p in fr["joints"].items()}
    return {
        "format":"exercise-private-rig-preview-v1",
        "exercise_id":record["exercise_id"],
        "source_sha256":src["sha256"],
        "source_label":src["label"],
        "frames":frames,
        "fps":fps,
        "review_status":"pending",
        "technique_certified":False,
        "animation_purpose":"3D position preview only; not an instructional/approved GIF",
        "coordinate_conversion":"x, -depth, -vertical; floor alignment estimated from extremities",
        "validation":checks
    }
