# Captura de movimento por vídeo — fase opcional

**Estado:** infraestrutura implementada; nenhum vídeo real foi importado. Os materiais atuais continuam inalterados. Tudo funciona localmente, sem chaves da OpenAI e sem enviar vídeos ao GitHub.

## Como usar (quando houver um vídeo autorizado)

1. Grave ou obtenha autorização para um vídeo curto da variação exata do exercício, preferencialmente demonstrado por profissional. Corpo inteiro visível, câmera fixa, boa iluminação; use vista lateral para ponte, coice e exercícios no tapete.
2. Instale Python 3.11 e, em seu próprio computador, execute: pip install -r requirements-capture.txt. Esse pacote instala MediaPipe e OpenCV **apenas no computador**. Não será instalado no fluxo automático de GIFs.
3. Baixe você mesma um modelo pose_landmarker.task pelo [guia oficial do MediaPipe](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python). Não há download automático pelo repositório.
4. Coloque vídeo e modelo em work_private/, pasta excluída do Git.

Execute:

~~~bash
python scripts/extract_video_pose.py --video work_private/ponte.mp4 --model work_private/pose_landmarker.task --exercise-id ponte --source-label "Vídeo autorizado" --rights-confirmed --view lateral --out work_private/captures/ponte.json
python scripts/preview_capture.py --input work_private/captures/ponte.json --out work_private/previews/ponte.gif
~~~

## Validação automatizada

O sistema verifica o cadastro do exercício, declaração de permissão, hash SHA-256 da fonte, timestamps, pontos dentro da imagem, limiar mínimo de confiança, saltos excessivos e mudanças extremas de comprimento aparente dos membros. Se falhar, rejeita. Os testes automáticos geram apenas um exemplo **sintético e temporário para verificar o programa**, nunca uma demonstração publicada.

Essas verificações **não conseguem provar a técnica correta**, a correspondência entre o nome do exercício e o movimento, a segurança individual, a amplitude segura ou os direitos autorais reais. O GIF de prévia sempre mostra **NÃO VALIDADA** e fica fora das fichas públicas até revisão humana. Informações corporais extraídas de vídeos podem ser dados pessoais; não compartilhe automaticamente nem suba ao GitHub público. O software não envia nada à API da OpenAI.

## Próxima etapa

Somente quando tivermos vídeos autorizados e uma pessoa qualificada aprovar a execução: adaptar as articulações extraídas ao rig de uma personagem consistente no Blender, preservando a trajetória do vídeo. A simples existência de pontos 2D não oferece biomecânica 3D perfeita.
