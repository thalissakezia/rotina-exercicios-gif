# Qualidade de imagem e movimento: normas para geração

## Hierarquia de referências
1. Vídeo de execução de demonstrador qualificado e com direitos de uso verificados, quando disponível.
2. Captura de pose de vídeo REAL (MediaPipe/MMPose/FreeMoCap/Pose2Sim), analisada por pessoa qualificada.
3. Animação 3D com articulações constrangidas, usando rig com proporções constantes (Blender).
4. Ilustrações em poses de fonte documentada (Workout Guide) — **o modo atual**, somente três poses.
5. Nunca pedir à IA generativa para inventar os quadros intermediários e tratar como instrução fisioterapêutica.

## Checklist por exercício
- ID, nome e vídeo/imagem de origem correspondem ao MESMO exercício e à MESMA variação.
- Posição inicial, pico e retorno permitem compreender o movimento; os pés/joelhos/cotovelos não desaparecem.
- Proporção corporal constante, membros não duplicados, câmera fixa e nenhum objeto adicional imprevisto.
- Pelve e coluna não fazem movimentos visivelmente incompatíveis com a instrução.
- Braços/pernas correspondem à variação: elevação interna levanta a PERNA DE BAIXO; elevação lateral levanta a DE CIMA.
- As imagens de músculos são apenas mapas ilustrativos e devem mostrar grupos primários, sem inventar precisão anatômica.
- GIF reproduzido de verdade com múltiplos quadros; textos e ângulos não devem ficar cortados.
- Em movimentos isométricos (prancha), o corpo pode ficar PARADO durante toda a duração. Não animar repetição inexistente.
- A checagem automática pode verificar existência de quadros, corte e correspondência de IDs, **não** certificar segurança da técnica. Revisão humana é obrigatória para alegação de correção biomecânica.

## Ferramentas adicionais (sem instalações compulsórias)
Veja `data/fontes_tecnicas.json`. MediaPipe, MMPose e Pose2Sim são para extrair movimento de vídeos reais autorizados; Blender importa dados e renderiza personagem; OpenSim pode estimar movimento e forças em pipelines especializados. Nenhuma dessas ferramentas fornece confirmação automática de execução perfeita nem IA gratuita ilimitada.

## Custos e segurança
Nenhuma chave OpenAI é necessária no modo atual. ChatGPT Plus não disponibiliza créditos nem uma chave gratuita para a API. Se um dia optar por pagar uso da API, crie a chave em `https://platform.openai.com/api-keys` e guarde-a em **GitHub → repositório → Settings → Secrets and variables → Actions → New repository secret**, nome `OPENAI_API_KEY`. Nunca em arquivo ou pasta do repositório, ainda que privada. NÃO ativar chamadas pagas na automação sem solicitação expressa.


## Três demonstrações geométricas experimentais

As animações de `interna`, `prancha-joelhos` e `gluteo-sentado` são desenhos **originais de código**, não imagens copiadas do ACE, NHS ou Harvard. O movimento é limitado por pontos 2D definidos manualmente. Em adução, move-se a perna inferior e a superior mantém-se dobrada; na prancha, a figura permanece imóvel e somente o ícone de respiração muda; no alongamento sentado, o tronco permanece ereto e o joelho se aproxima discretamente do peito. As representações não identificam toda a anatomia em 3D nem garantem que uma pessoa deva executar a mesma amplitude.

Fontes **apenas para instrução técnica** (imagens/fotografias das fontes não foram copiadas):
- Adutores: https://www.acefitness.org/resources/everyone/exercise-library/39/side-lying-hip-adduction/
- Prancha de joelhos: https://www.health.harvard.edu/healthy-aging-and-longevity/try-this-move-for-better-core-strength
- Glúteos sentado: https://www.cuh.nhs.uk/patient-information/stretches-for-the-hip/

**Estado:** demonstrações geradas automaticamente e verificadas quanto a frames/arquivos; a aprovação biomecânica permanece pendente.

**Revisão geométrica interna:** `scripts/test_procedural.py` mede distância do joelho ao tapete, colinearidade ombro–quadril–joelho, deslocamento da perna inferior e verticalidade do tronco sentado. São testes mínimos, não medem contato real com o solo, forças, dor, nem competência clínica.
