#!/usr/bin/env python3
"""Verifica coerência do catálogo e dos sete dias."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAYS = ("segunda","terca","quarta","quinta","sexta","sabado","domingo")

def validate():
    data = json.loads((ROOT/"data/exercicios.json").read_text(encoding="utf-8"))
    entries = data["exercicios"]
    index = {e["id"]:e for e in entries}
    assert len(index)==len(entries), "ID repetido no catálogo"
    for e in entries:
        assert e["nome"] and e["instrucoes"] and e["musculos"]
        assert e["status"] in ("referenciado","revisao_pendente","procedural_review")
        assert (e["slug"] is not None)==(e["status"]=="referenciado")
        if e["status"]=="procedural_review":assert e.get("reference_url") and e.get("drawing_kind")==e["id"]
    for day in DAYS:
        d=json.loads((ROOT/"data/dias"/(day+".json")).read_text(encoding="utf-8"))
        assert d["dia"]==day and d["exercicios"]
        seen=set()
        for item in d["exercicios"]:
            assert item["id"] in index, "Exercício desconhecido: "+item["id"]
            assert item["id"] not in seen, "Exercício duplicado no dia: "+day
            assert item["series"]>=1 and item["dose"]
            seen.add(item["id"])
    print("OK: "+str(len(entries))+" exercícios; 7 dias.")
    print("Referências pendentes: "+", ".join(e["nome"] for e in entries if e["status"]=="revisao_pendente"))

if __name__=="__main__":
    validate()
