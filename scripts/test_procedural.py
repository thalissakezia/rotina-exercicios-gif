#!/usr/bin/env python3
"""Testes de geometria e continuidade do piloto; NÃO avaliam segurança clínica."""
from math import hypot
from procedural import (PLANK_POINTS, SEATED_TORSO, build,
                        inner_landmarks, seated_landmarks, eased)

N=12
def dist(a,b):
    return hypot(a[0]-b[0],a[1]-b[1])

p=PLANK_POINTS
assert 0 <= p["mat_top"]-p["knee"][1] <= 12, "Joelho fora do tapete"
shoulder,hip,knee=p["shoulder"],p["hip"],p["knee"]
predicted=shoulder[1]+(knee[1]-shoulder[1])*(hip[0]-shoulder[0])/(knee[0]-shoulder[0])
assert abs(hip[1]-predicted)<=6, "Quadril fora do alinhamento"
assert abs(SEATED_TORSO["hip"][0]-SEATED_TORSO["shoulder"][0])<=12

for make in (inner_landmarks,seated_landmarks):
    seq=[make(eased(i,N)) for i in range(N)]
    sizes=[(dist(t[0],t[1]),dist(t[1],t[2]),dist(t[2],t[3])) for t in seq]
    for dimensions in sizes:
        assert all(abs(a-b)<0.00001 for a,b in zip(dimensions,sizes[0])), "Membro alongou/encolheu"
    for k in range(N):
        cur,nxt=seq[k],seq[(k+1)%N]
        assert all(dist(a,b)<12 for a,b in zip(cur,nxt)), "Salto de articulação"
    assert dist(seq[0][2],seq[N//2][2])>9, "Movimento imperceptível"
assert inner_landmarks(1)[2][1]<inner_landmarks(0)[2][1], "Movimento da perna inferior invertido"
assert len({round(eased(i,N),6) for i in range(N)})>=6
for eid in ("interna","prancha-joelhos","gluteo-sentado"):
    frames=build(eid,N)
    assert len(frames)==N
    assert all(img.size==(335,335) and img.getbbox() for img in frames)
    assert len({img.tobytes() for img in frames})>=9, "Poucos quadros diferentes"
plank=build("prancha-joelhos",N)
fixed=plank[0].crop((0,140,335,335)).tobytes()
assert all(im.crop((0,140,335,335)).tobytes()==fixed for im in plank), "Corpo mexendo na prancha isométrica"
print("OK: 12 quadros, velocidade suave, comprimento constante e prancha estática.")
