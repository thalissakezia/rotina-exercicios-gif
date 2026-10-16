#!/usr/bin/env python3
"""Testes geométricos básicos para poses desenhadas localmente.
Não constituem validação clínica nem inferência por IA.
"""
from procedural import PLANK_POINTS, INNER_LOWER_ANKLES, SEATED_TORSO, build

p=PLANK_POINTS
assert p["mat_top"]-p["knee"][1] <= 12, "Joelho fora do tapete na prancha"
assert 0<=p["mat_top"]-p["knee"][1], "Joelho deve ficar na superfície do tapete"
shoulder,hip,knee=p["shoulder"],p["hip"],p["knee"]
expected=shoulder[1]+(knee[1]-shoulder[1])*(hip[0]-shoulder[0])/(knee[0]-shoulder[0])
assert abs(hip[1]-expected)<=6, "Quadril fora do alinhamento ombro-joelho"
assert len({pt[1] for pt in INNER_LOWER_ANKLES})==3, "Perna inferior não muda de altura"
assert INNER_LOWER_ANKLES[2][1]<INNER_LOWER_ANKLES[0][1], "Direção da adução inválida"
assert abs(SEATED_TORSO["hip"][0]-SEATED_TORSO["shoulder"][0])<=12, "Tronco sentado inclinado demais"
for key in ("interna","prancha-joelhos","gluteo-sentado"):
    ims=build(key)
    assert len(ims)==3
    assert all(i.size==(335,335) for i in ims)
    assert all(i.getbbox() for i in ims)
print("OK: pontos 2D do tapete, apoio de joelho, perna inferior e tronco sentado validados.")
