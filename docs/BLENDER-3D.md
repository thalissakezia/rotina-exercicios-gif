# Prévia 3D padronizada — implementação experimental

**Estado:** o código de captura/transformação 3D e o gerador de manequim foram implementados. Nenhum vídeo real foi importado, e nenhum modelo humano/rig profissional foi criado ou aprovado. O gerador Blender não roda no GitHub Actions; exige Blender localmente. Os testes do Actions cobrem geometria sintética e sintaxe do script, não a renderização no Blender.

## Fluxo quando houver um vídeo autorizado

1. Obtenha demonstração real da **variação exata** do exercício, com permissão de uso, câmera fixa e corpo visível.
2. No computador com Python 3.11, instale dependências opcionais: `pip install -r requirements-capture.txt` e obtenha o modelo `.task` pela documentação oficial do MediaPipe.
3. Execute `extract_video_pose.py`, como explicado em [CAPTURA-DE-MOVIMENTO.md](CAPTURA-DE-MOVIMENTO.md). O programa guarda também coordenadas `world_landmarks` quando o MediaPipe as oferece.
4. Converta para coordenadas de prévia:

```bash
python scripts/prepare_blender_motion.py --input work_private/captures/ponte.json --out work_private/rig/ponte.json
```

5. Com Blender instalado, execute:

```bash
blender --background --python scripts/blender_preview.py -- --input work_private/rig/ponte.json --out work_private/rig/ponte_PREVIEW_NOT_VALIDATED.blend --render-still
```

O Blender cria **um manequim geométrico** com segmentos e articulações animados e câmera fixa, mais uma imagem de conferência opcional. Essa etapa NÃO produz automaticamente GIF instrucional: é preciso validar o movimento primeiro.

## Limitações e segurança

- Estimativa 3D de câmera única pode ter profundidade incorreta e membros que parecem alongar/encolher. Os controles sinalizam grandes erros, mas não tornam o movimento clinicamente exato.
- O piso é estimado a partir do ponto mais baixo de extremidades observadas; não é medição física do contato com o tapete.
- Posição da cabeça é aproximada e o modelo é um manequim técnico, não a personagem feminina final.
- `work_private/` está no `.gitignore`: não inclua dados corporais, vídeos, identidade de pessoas ou modelos `.task` no GitHub público.
- Vídeos de terceiros devem ter autorização explícita; repositórios de GIFs com direitos incertos não são fontes automaticamente válidas.
- O arquivo `.blend` é apenas uma **prévia não validada**, sem certificação de execução biomecânica.
- Não há custo de API OpenAI obrigatório.

## Verificações

`scripts/test_world3d.py` exercita dados *sintéticos* e rejeita saltos/corpos inconsistentes. A pipeline do GitHub valida a sintaxe do Blender via `py_compile`, mas não instala nem executa o Blender. A verificação real de renderização e a avaliação da técnica precisam acontecer numa etapa posterior.
