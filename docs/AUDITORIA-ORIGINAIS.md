# Conferência das sete fichas originais

Foram comparadas **33 posições** (5+4+4+5+5+6+4). Cada posição é vinculada ao cadastro de um dia em `data/originais.json` e `data/dias`.

- **Substituições por falta de referência visual:** agachamento sumô → agachamento sem carga (segunda); agachamento sumô → afundo lateral (quinta e sábado). **Não são técnicas idênticas.** Ambos são movimentos de coxas/glúteos, e o afundo lateral também trabalha adutores.
- **Adaptações de mobilidade:** caminhada rápida na quarta foi representada com base de caminhada; alongamento posterior de coxa na quarta passou para a versão sentada; mobilidade de ombros foi parcialmente representada por círculos de braços; domingo separou ombros e peitoral.
- **Recuperados após nova busca:** abdominal bicicleta lento na sexta (fonte `bicycle-crunch`), alongamento posterior de coxa na quarta e alongamento de peitoral no domingo (`doorway-chest-stretch`).
- **Ainda sem imagem técnica equivalente:** elevação interna de perna (segunda/quinta); prancha com joelhos apoiados (terça/sexta/sábado); alongamento de glúteos sentado (quarta/domingo). Eles **constam na rotina**, mas o gerador registra pendência visual e não inventa movimentos.
- **Complementos de postura:** elevação Y/T, gato-vaca, concha lateral, mobilidade e alongamentos adicionais. Eles não contam como correspondência automática dos exercícios originais.

**Regra:** nunca substituir um exercício de adutores por movimento exclusivamente de abdutores; nunca representar uma prancha sobre os pés como a versão com joelhos apoiados; nunca marcar uma imagem estática como demonstração completa do movimento.

O comando `python scripts/audit_originais.py` verifica mecanicamente se as 33 posições estão preservadas por um ID ou por uma substituição documentada.
