#!/usr/bin/env python3
"""Offline provenance gate for manual review; NEVER makes clinical judgments.

Even an accepted record only says a human *declared* these reviews.
It NEVER promotes or publishes a private preview automatically.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime
from capture_utils import CaptureError, catalog_ids, validate_capture

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=(ROOT/"work_private").resolve()
CHECKS=(
  "rights_and_consent_verified","exercise_variant_matches","starting_pose_checked",
  "joint_alignment_checked","pelvis_spine_checked","range_of_motion_checked",
  "return_phase_checked","no_visible_anatomy_errors","frame_by_frame_checked",
  "suitable_for_mat_exercise"
)

def digest(path):
    result=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):result.update(block)
    return result.hexdigest()

def gate(record,capture,permissions,valid_ids,preview_hash):
    cap_quality=validate_capture(capture,valid_ids)
    eid=capture["exercise_id"]
    if record.get("schema_version")!=1 or record.get("exercise_id")!=eid:
        raise CaptureError("Revisao nao corresponde ao mesmo exercicio")
    if record.get("source_sha256")!=capture["source"]["sha256"]:
        raise CaptureError("Hash do video na revisao difere da captura")
    if record.get("preview_sha256")!=preview_hash:
        raise CaptureError("GIF de previa mudou desde a revisao")
    permissions=permissions.get("exercises",{})
    right=permissions.get(eid,{})
    if not (right.get("permission_confirmed") is True
            and right.get("person_consented") is True):
        raise CaptureError("Direitos e consentimento nao confirmados")
    if right.get("basis") not in ("own_recording","written_license","cc_license"):
        raise CaptureError("Origem dos direitos insuficiente")
    if right.get("basis")=="cc_license" and not str(right.get("license_url","")).startswith("https://"):
        raise CaptureError("Link da licenca obrigatorio")
    if not right.get("source_label") or right["source_label"]!=capture["source"]["label"]:
        raise CaptureError("Origem da captura e manifestos incompatíveis")
    if record.get("decision")!="approve_for_private_staging":
        raise CaptureError("Decisao explicita da revisao ainda ausente")
    reviewer=record.get("reviewer")
    if not isinstance(reviewer,dict) or not all(
        isinstance(reviewer.get(field),str) and len(reviewer[field].strip())>=3
        for field in ("name","qualification","notes")):
        raise CaptureError("Responsavel e justificativa da revisao obrigatorios")
    try:
        timestamp=datetime.fromisoformat(record.get("reviewed_at","").replace("Z","+00:00"))
        if timestamp.tzinfo is None:raise ValueError
    except ValueError:raise CaptureError("Data da revisao precisa ser ISO com fuso horario")
    checks=record.get("checklist")
    if not isinstance(checks,dict) or set(checks)!=set(CHECKS) or any(checks[k] is not True for k in CHECKS):
        raise CaptureError("Todos os criterios devem ter aceite manual explicito")
    if record.get("synthetic_test_only") is True or capture.get("synthetic_test_only") is True:
        raise CaptureError("Capturas sinteticas nunca sao material de treino")
    return {"exercise_id":eid,"status":"eligible_for_manual_private_staging",
            "automatic_publication":False,"clinical_certification_automated":False,
            "source_sha256":record["source_sha256"],"preview_sha256":preview_hash,
            "frame_count":cap_quality["frames"]}

def private(path):
    p=Path(path).resolve()
    if PRIVATE not in p.parents:raise CaptureError("Arquivos sensiveis devem ficar em work_private/")
    return p

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--capture",type=Path,required=True)
    p.add_argument("--preview",type=Path,required=True)
    p.add_argument("--permissions",type=Path,required=True)
    p.add_argument("--review",type=Path,required=True)
    args=p.parse_args()
    try:
        cap=private(args.capture);preview=private(args.preview)
        perms=private(args.permissions);review=private(args.review)
        result=gate(
            json.loads(review.read_text(encoding="utf-8")),
            json.loads(cap.read_text(encoding="utf-8")),
            json.loads(perms.read_text(encoding="utf-8")),
            catalog_ids(ROOT),digest(preview))
    except (CaptureError,ValueError,FileNotFoundError,json.JSONDecodeError) as e:
        p.error(str(e))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    print("Nenhum arquivo publicado. Revisor/credenciais são informados por humanos, não comprovados por software.")

if __name__=="__main__":main()
