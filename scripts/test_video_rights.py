#!/usr/bin/env python3
"""Assures video usage stays opt-in and never claims unknown rights."""
import json
from pathlib import Path
from plan_captures import make_plan

ROOT=Path(__file__).resolve().parents[1]
obj=json.loads((ROOT/"data/fontes_de_video.json").read_text(encoding="utf-8"))
assert obj["schema_version"]==1
assert len(obj["sources"])>=3
for src in obj["sources"]:
    assert src["allowed_for_render"] is False
    assert src["reason"] and src["url"] and src["rights"]
    assert src["media"] and src["id"]
plan=make_plan()
assert plan["total_exercicios_distintos"]>=20
assert plan["total_ocorrencias"]>=33
assert len({p["id"] for p in plan["exercicios"]})==len(plan["exercicios"])
assert all(not p["publicacao_permitida"] and p["revisao_movimento"]=="pendente"
           and p["direitos_video"]=="não verificados" for p in plan["exercicios"])
assert plan["exercicios"][0]["id"] in {"ponte","coice","agachamento","flexao","birddog","deadbug","lateral","interna"}
print("OK: fila automatizada priorizada, nenhuma fonte de vídeo aprovada sem direitos claros.")
