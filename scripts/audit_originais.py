#!/usr/bin/env python3
"""Impede omissão silenciosa dos exercícios nas sete fichas originais."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
orig=json.loads((ROOT/"data/originais.json").read_text(encoding="utf-8"))["dias"]
cat=json.loads((ROOT/"data/exercicios.json").read_text(encoding="utf-8"))
lookup={e["id"]:e for e in cat["exercicios"]}
expected_count={"segunda":5,"terca":4,"quarta":4,"quinta":5,"sexta":5,"sabado":6,"domingo":4}
allowed={"mantido","adaptado","substituido","pendente"}
num=0
for day,count in expected_count.items():
    row=orig[day]["originais"]
    assert len(row)==count, f"{day}: esperados {count}, registrados {len(row)}"
    cur=json.loads((ROOT/f"data/dias/{day}.json").read_text(encoding="utf-8"))
    ids={item["id"] for item in cur["exercicios"]}
    for original in row:
        num+=1
        assert original["id"] in ids, f"Exercício original perdido: {day}/{original['nome']}"
        assert original["id"] in lookup, f"Sem cadastro: {original['id']}"
        assert original["status"] in allowed
        if original["status"]!="mantido":assert original.get("observacao"),f"Justificativa faltando: {day}/{original['nome']}"
        if original["status"]=="pendente":assert lookup[original["id"]]["status"] in ("revisao_pendente","procedural_review"),f"Pendente sem bloqueio: {original['id']}"
        for extra in original.get("extras",[]):assert extra in ids,f"Faltou parte do exercício combinado: {day}/{extra}"
print(f"OK: {num} exercícios originais rastreados, nenhum perdido sem substituição/pendência documentada.")
