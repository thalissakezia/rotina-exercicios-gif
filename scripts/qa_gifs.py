#!/usr/bin/env python3
"""Auditoria automática de arquivos GIF e geração de relatório técnico legível."""
import json
from pathlib import Path
from PIL import Image, ImageSequence

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output"
DAYS=("segunda","terca","quarta","quinta","sexta","sabado","domingo")
all_ex=json.loads((ROOT/"data/exercicios.json").read_text(encoding="utf-8"))["exercicios"]
index={x["id"]:x for x in all_ex}
report={"resultado":"verificacao_digital_nao_biomecanica","checagens":[],"pendencias":[],"avisos":[]}
errors=[]

def inspect(p,label):
    if not p.exists():
        errors.append(f"Não existe: {p.relative_to(ROOT)}")
        return
    try:
        with Image.open(p) as im:
            n=im.n_frames
            width,height=im.size
            frames=[]
            for fr in ImageSequence.Iterator(im):
                frames.append(fr.convert("RGB").resize((32,32)))
            moving=any(im2.tobytes()!=frames[0].tobytes() for im2 in frames[1:])
            if n<2:errors.append(f"Sem animação (quadros insuficientes): {label}")
            if width<300 or height<300:errors.append(f"Dimensão baixa: {label}")
            if not moving:report["avisos"].append(f"Não há mudança visual mensurável: {label}")
            report["checagens"].append({"arquivo":str(p.relative_to(ROOT)),"tipo":label,"quadros":n,"largura":width,"altura":height,"mudanca_detectada":moving})
    except Exception as e:
        errors.append(f"Arquivo GIF ilegível: {label}: {e}")

for day in DAYS:
    inspect(OUT/"daily"/(day+".gif"),"dia_"+day)
    items=json.loads((ROOT/"data/dias"/(day+".json")).read_text(encoding="utf-8"))["exercicios"]
    for it in items:
        ex=index[it["id"]]
        if ex["status"]=="referenciado":
            inspect(OUT/"gifs"/day/(it["id"]+".gif"),day+"/"+it["id"])
        else:
            report["pendencias"].append({"dia":day,"id":it["id"],"nome":ex["nome"],"motivo":"sem referência visual exata; GIF individual não produzido"})
report["erros"]=errors
report["contagem"]={"verificados":len(report["checagens"]),"pendentes":len(report["pendencias"]),"erros":len(errors),"avisos":len(report["avisos"])}
(OUT/"quality_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report["contagem"],ensure_ascii=False))
if errors:raise SystemExit("\n".join(errors))
