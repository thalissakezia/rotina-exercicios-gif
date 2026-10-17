#!/usr/bin/env python3
"""Tests: never process a video merely because it exists in a folder."""
import tempfile
from pathlib import Path
from batch_capture import candidates

ids={"ponte","coice"}
with tempfile.TemporaryDirectory() as folder:
    d=Path(folder)
    (d/"ponte.mp4").write_bytes(b"dummy")
    (d/"coice.mov").write_bytes(b"dummy")
    (d/"unknown.mp4").write_bytes(b"dummy")
    rights={
        "ponte":{"permission_confirmed":True,"person_consented":True,
                 "basis":"own_recording","source_label":"Recording with consent","view":"lateral"},
        "coice":{"permission_confirmed":False,"person_consented":True,
                 "basis":"written_license","source_label":"Unverified","view":"lateral"},
    }
    cases=candidates(d,rights,ids)
    by={x["exercise_id"]:x for x in cases}
    assert len(cases)==3
    assert by["ponte"]["ready_for_local_preview"]
    assert not by["coice"]["ready_for_local_preview"]
    assert not by["unknown"]["ready_for_local_preview"]
    rights["ponte"]["person_consented"]=False
    assert not next(x for x in candidates(d,rights,ids)
                    if x["exercise_id"]=="ponte")["ready_for_local_preview"]
    rights["ponte"]["person_consented"]=True
    rights["ponte"]["basis"]="cc_license"
    assert not next(x for x in candidates(d,rights,ids)
                    if x["exercise_id"]=="ponte")["ready_for_local_preview"]
print("OK: execução em lote bloqueia vídeos não autorizados, sem consentimento ou licença documentada.")
