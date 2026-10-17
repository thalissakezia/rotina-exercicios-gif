# Próxima etapa: biblioteca de referências reais e fila de captura

O projeto já consegue capturar coordenadas 2D/3D com MediaPipe, gerar uma prévia e montar um manequim Blender. Isso NÃO significa que temos movimentos reais licenciados ou avaliados.

## O que foi preparado

- [Fonte e direitos](../data/fontes_de_video.json): biblioteca de fontes analisadas, cada uma com status e motivo de aceitação ou bloqueio.
- [Fila automática](../output/capture_plan.json): exercícios distintos ordenados por prioridade e frequência. Regenerada a partir dos sete JSONs semanais; o topo inclui ponte e coice de glúteos, seguidos de exercícios frequentes e relevantes ao objetivo.
- [Captura local](CAPTURA-DE-MOVIMENTO.md): vídeos autorizados ficam apenas em `work_private/`; não são enviados ao GitHub.
- [Manequim Blender](BLENDER-3D.md): gera prévia geométrica 3D, não uma figura humana clinicamente certificada.

## Exigências antes de produzir um GIF real

1. Obter uma filmagem autêntica de **variação idêntica** com licença explícita para derivação/redistribuição ou autorização do próprio titular e consentimento da pessoa filmada.
2. Confirmar execução com profissional qualificado, observando anatomia, controle da pelve/coluna e posicionamento no tapete. A revisão humana é essencial.
3. Capturar coordenadas e revisar erros de estimativa em vídeos de frente/lado quando necessário.
4. Testar o Blender com renderização real e inspecionar os quadros.
5. Apenas após aprovação, criar uma personagem padronizada e integrar às fichas do dia — jamais publicar automaticamente uma prévia como GIF validado.

**Fonte descartada:** a Free Exercise DB with Videos tem metadados/código MIT, mas o próprio README afirma não saber a proveniência dos vídeos. A York St John University proíbe redistribuição. O arquivo Glute-bridge.png do Wikimedia Commons é estático; possuir licença permissiva não o transforma em fonte de movimento real.

O projeto continuará sem API paga. Não usar o GitHub público para armazenar vídeo identificável sem autorização expressa.

## Candidatos de vídeos gratuitos encontrados (não importados)

- [Pexels: ponte de glúteos, 7 s](https://www.pexels.com/video/woman-doing-glute-bridge-exercise-6525487/) — licença Pexels permite modificações; revisar variante exata, enquadramento e uso da imagem da pessoa.
- [Pexels: coice, 11 s](https://www.pexels.com/video/woman-doing-donkey-kick-exercise-10740728/) — gravado em plataforma/caminhão, não sobre tapete, portanto pode não atender nossa variação.
- [DVIDS: Donkey Kick](https://www.dvidshub.net/video/677352/donkey-kick) — marcado domínio público, mas o aviso preserva direitos de imagem e proíbe implicar endosso. Não usar automaticamente.
- [DVIDS: One Minute Glute Bridge Challenge](https://www.dvidshub.net/video/757660/one-minute-glute-bridge-challenge) — contém partes com restrição de distribuição. Não importar.

Cada candidato está registrado em `data/fontes_de_video.json` com `allowed_for_render:false`. Nenhum arquivo foi baixado ou distribuído. A escolha final requer revisão de técnica e direitos; possuir licença de uso não significa que a postura do exercício esteja correta.
