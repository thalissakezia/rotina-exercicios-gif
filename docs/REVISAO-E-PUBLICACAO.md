# Revisão e integração: aprovação humana obrigatória

Esta é a ponte entre **capturas reais privadas** e os arquivos didáticos finais. Sem filmagens autorizadas e revisão humana, nenhuma captura é promovida.

## 1. Obter uma prévia completa do Blender

Depois de capturar coordenadas reais com licença/consentimento verificados e gerar o arquivo `.blend` conforme [BLENDER-3D.md](BLENDER-3D.md), renderize todos os quadros localmente:

```bash
mkdir -p work_private/frames work_private/review
blender --background work_private/rig/ponte_PREVIEW_NOT_VALIDATED.blend -o //../frames/review_ -a
python scripts/render_review_gif.py --frames-dir work_private/frames --prefix review_ --out work_private/review/ponte.gif --contact-sheet work_private/review/ponte-sheet.png
```

O GIF terá **aviso visível "PRÉVIA 3D - NÃO VALIDADA"**, e a folha mostrará seis posições representativas. Esse material não deve entrar em `output/gifs` antes de revisão real da técnica.

## 2. Revisão explícita

Crie em `work_private/` um manifesto de permissões com licença, consentimento, origem e a variação correta; veja [LOTE-DE-VIDEOS.md](LOTE-DE-VIDEOS.md).

Registre a aprovação humana em `work_private/reviews/ponte.json` (não enviar ao GitHub):

```json
{
  "schema_version": 1,
  "exercise_id": "ponte",
  "source_sha256": "hash SHA256 do video original",
  "preview_sha256": "hash SHA256 do GIF revisado",
  "decision": "approve_for_private_staging",
  "reviewed_at": "2026-10-17T12:00:00-03:00",
  "reviewer": {
    "name": "Nome completo da pessoa que revisou",
    "qualification": "Qualificação profissional informada",
    "notes": "Descrever o que foi verificado no movimento"
  },
  "checklist": {
    "rights_and_consent_verified": true,
    "exercise_variant_matches": true,
    "starting_pose_checked": true,
    "joint_alignment_checked": true,
    "pelvis_spine_checked": true,
    "range_of_motion_checked": true,
    "return_phase_checked": true,
    "no_visible_anatomy_errors": true,
    "frame_by_frame_checked": true,
    "suitable_for_mat_exercise": true
  }
}
```

Os hashes devem ser calculados a partir dos arquivos reais; não reutilize valores de exemplo.

Execute:

```bash
python scripts/approval_gate.py --capture work_private/captures/ponte.json --preview work_private/review/ponte.gif --permissions work_private/video_permissions.json --review work_private/reviews/ponte.json
```

Se algum documento, licença, variação ou verificação estiver ausente, a etapa é **bloqueada**. Mesmo se passar, a saída só diz `eligible_for_manual_private_staging`: **o software não confirma qualidade biomecânica nem publica GIFs.** Ele verifica consistência de metadados informados, não a validade jurídica do consentimento ou a formação do profissional.

## 3. Próxima condição

A decisão de publicar requer inspeção final real do GIF e da ficha, com atribuição/condições da licença aplicadas, autorização explícita da dona do projeto para subir ao repositório público e revisão da execução por pessoa qualificada.

## Testes e privacidade

- `scripts/test_review_gate.py` roda em GitHub Actions com **quadros sintéticos** para verificar controles, sem salvar GIFs de teste no projeto.
- O workflow [Testar Blender 3D real (dados sintéticos)](../.github/workflows/testar-blender-3d.yml) executa Blender de fato e renderiza 12 quadros, monta GIF e folha de inspeção, e os descarta ao terminar o job.
- Não usar IA para inventar frames e rotular como técnica comprovada.
- Nada é enviado à OpenAI, e nenhum serviço externo pago é obrigatório.
