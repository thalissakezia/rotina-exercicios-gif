#!/usr/bin/env python3
"""Plan a batch of authorized video captures; never download or approve sources."""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DAYS=("segunda","terca","quarta","quinta","sexta","sabado","domingo")
FOCUS=("ponte","coice","agachamento","flexao","birddog","deadbug","lateral","interna")
VIEWS={
    "ponte":"lateral","coice":"lateral","agachamento":"obliqua",
    "flexao":"lateral","birddog":"lateral","interna":"frontal",
    "lateral":"frontal","deadbug":"lateral"
}
def make_plan():
    ex=json.loads((ROOT/"data/exercicios.json").read_text(encoding="utf-8"))["exercicios"]
    catalog={x["id"]:x for x in ex}
    counts=Counter(); schedule={}
    for day in DAYS:
        obj=json.loads((ROOT/"data/dias"/f"{day}.json").read_text(encoding="utf-8"))
        for row in obj["exercicios"]:
            counts[row["id"]]+=1
            schedule.setdefault(row["id"],[]).append(day)
    items=[]
    for eid,n in counts.items():
        e=catalog[eid]
        items.append({
          "id":eid,"nome":e["nome"],"dias":schedule[eid],
          "vezes_na_semana":n,
          "prioridade":(-2 if eid=="ponte" else -1 if eid=="coice" else 0 if eid in FOCUS else 1),
          "visao_sugerida":VIEWS.get(eid,"lateral"),
          "origem_video":"não fornecida",
          "direitos_video":"não verificados",
          "captura_real":"não iniciada",
          "revisao_movimento":"pendente",
          "publicacao_permitida":False,
          "musculos":e["musculos"]
        })
    items.sort(key=lambda x:(x["prioridade"],-x["vezes_na_semana"],x["nome"]))
    return {"schema_version":1,"objetivo":"capturar vídeo autorizado, avaliar forma, produzir avatar padronizado",
            "nao_inferir_que_esta_aprovado":True,
            "total_exercicios_distintos":len(items),
            "total_ocorrencias":sum(counts.values()),"exercicios":items}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=ROOT/"output/capture_plan.json")
    a=p.parse_args()
    data=make_plan()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"OK: fila de captura: {data['total_exercicios_distintos']} exercícios distintos; todos aguardam fonte autorizada.")
