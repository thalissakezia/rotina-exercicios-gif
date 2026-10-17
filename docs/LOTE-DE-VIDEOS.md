# Importar vídeos em lote — sem APIs pagas

Esta fase mantém tudo local: basta reunir vídeos próprios ou com autorização comprovada, para que o projeto prepare as prévias automaticamente, sem precisar pedir cada exercício isoladamente.

**Não há nenhum vídeo aprovado no repositório até o momento.** Não reutilize vídeos de bases sem direitos claros. A automação do GitHub não baixa nem armazena filmagens.

## Preparação

1. Instale opcionalmente `pip install -r requirements-capture.txt` e obtenha um modelo `pose_landmarker.task` oficial do MediaPipe.
2. Armazene os vídeos em `work_private/videos/` com o nome exato do ID, por exemplo `ponte.mp4` ou `coice.mov`.
3. Crie `work_private/video_permissions.json` (fora do Git) com autorizações específicas:

```json
{"schema_version":1,"exercises":{"ponte":{"permission_confirmed":true,"person_consented":true,"basis":"own_recording","source_label":"Filmagem própria autorizada","view":"lateral"}}}
```

O programa verifica os campos declarados, mas não consegue comprovar juridicamente o consentimento, a titularidade do vídeo nem o movimento correto. Você precisa ter os direitos e o consentimento de fato.

## Executar

```bash
python scripts/batch_capture.py
python scripts/batch_capture.py --run
```

Sem `--run`, mostra a lista de candidatos bloqueados e aptos. Com `--run`, extrai o movimento de todos os vídeos autorizados, prepara os arquivos `work_private/captures/<id>.json` e `work_private/rig/<id>.json`. Todos continuam marcados **pendentes de avaliação técnica**. Não gera GIF público, não publica nenhum dado pessoal nem executa a API da OpenAI.

Se houver vídeo com erro de detecção, a execução falhará para não inventar articulações. Próxima etapa depois de capturas reais: inspeção profissional e composição de personagem Blender nos cartões animados.
